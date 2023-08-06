import time
import json
import sys
import asyncio
import ssl
from typing import Union, Any, NoReturn, Optional
from datetime import datetime as dt

from .exception import VkErr
from .tools import peer
from .dot_dict import DotDict

import aiohttp


class Api:
    """
    Make API requests and
    API-helpers handler.

    Contain main info like
    access_token,
    version and etc.
    """
    def __init__(
            self,
            token: str,
            v: Union[str, float],
            group_id: int = 0
        ) -> None:
        self.url = 'https://api.vk.com/method/'
        self.token = token
        self.v = str(v)
        self.group_id = abs(group_id)
        self.type = 'group' if self.group_id else 'user'
        self.session = aiohttp.ClientSession()
        self.ssl = ssl.SSLContext()
        self._last_request_time = time.time()
        self._freeze_time = 1 / 3 if self.type == 'user' else 1 / 20
        self._method = None

    def __rshift__(self, cls):
        cls.api = self
        return cls

    def __getattr__(self, value: str):
        self.method = value
        return self

    async def __call__(self, **kwargs) -> DotDict:
        """
        Make every API requests
        """
        return await self.request(self.method, data=kwargs)

    async def request(self, method: str, data: dict) -> DotDict:
        """
        Make every API requests
        """
        api_data = {
            'access_token': self.token,
            'v': self.v,
            **data
        }

        self._request_wait()

        async with self.session.post(self.url + method, data=api_data, ssl=self.ssl) as r:
            resp = await r.json()

        if 'error' in resp:
            raise VkErr(resp)
        else:
            if isinstance(resp['response'], dict):
                return DotDict(resp['response'])
            return resp['response']

    def _request_wait(self) -> None:
        """
        Pause between requests
        """
        now = time.time()
        diff = now - self._last_request_time

        if diff < self._freeze_time:
            time.sleep(self._freeze_time - diff)
            self._last_request_time = time.time()

    @property
    def method(self):
        """
        Method name
        """
    @method.getter
    def method(self) -> str:
        res = self._method
        self._method = None
        return res

    @method.setter
    def method(self, value: str) -> None:
        if self._method is None:
            self._method = value
        else:
            self._method += '.' + value

class LongPoll:
    """
    LongPoll scheme
    """
    user_get = {
        'need_pts': False,
        'lp_version': 3
    }
    user_init = {
        'wait': 25,
        'mode': 234,
        'version': 10
    }
    group_get = {
        # group_id
    }
    group_init = {
        'wait': 25
    }

    def __init__(self, faileds=[], default=True, **kwargs) -> None:
        self.faileds = faileds
        self.start_settings = kwargs
        self.reaction_handlers = []

    def __getattr__(self, event_name: str):
        """
        Get handling event
        """
        hand = ReactionHandler(event_name)
        self.reaction_handlers.append(hand)

        return hand

    async def _lp_start(self, default=True, **kwargs) -> NoReturn:

        ## Reactions tree
        self._reactions_init()

        if self.api.type == 'group':
            LongPoll.group_get['group_id'] = self.api.group_id

        self.start_settings = {
                **((LongPoll.user_get if self.api.type == 'user' else LongPoll.group_get) if default else {}),
                **self.start_settings
            }

        ## Yours settings
        self.lp_settings = {**(LongPoll.group_init if self.api.type == 'group' else LongPoll.group_get), **kwargs} if default else kwargs

        ## Intermediate lp params like server, ts and key
        self.lp_info = await self.api.request(
                method=self._method_name(),
                data=self.start_settings
            )
        self.start_time = dt.now()
        self.format_start = self.start_time.strftime("[%Y-%m-%d %H:%M:%S]")
        print(f"\033[2m{self.format_start} \033[0m\033[32mListening VK LongPoll...\033[0m")

        ## Stats
        self.events_get = 0
        self.events_handled = 0


        while True:
            ## Lp events

            lp_get = {
                'key': self.lp_info['key'],
                'ts': self.lp_info['ts']
            }

            data = {**lp_get, **self.lp_settings, 'act': 'a_check'}

            async with self.api.session.post(self.lp_info['server'], data=data, ssl=self.api.ssl) as response:
                self.lp = await response.json()

            res = self._failed_handler()
            if res is True:
                continue

            for update in self.lp['updates']:
                self.event = DotDict(update)
                self.events_get += 1
                if self.event.type in self.reactions:
                    self.events_handled += 1
                    self._reactions_get()
                    await self._reactions_call()

    def __call__(self, default=True, **kwargs) -> NoReturn:
        """
        Init LongPoll listening
        """
        try:
            loop = asyncio.get_event_loop()
            self.loop = loop
            loop.create_task(self._lp_start(default, **kwargs))
            loop.run_forever()

        except KeyboardInterrupt as err:
            end_time = dt.now()
            dif = end_time - self.start_time
            format_end = end_time.strftime("[%Y-%m-%d %H:%M:%S]")

            print(f"\n\033[2m{format_end} \033[0m\033[33mListening has been stoped\033[0m")
            print("Handled \033[36m%s\033[0m (\033[35m%.2f ps\033[0m)" % (
                self.events_handled,
                self.events_handled / dif.seconds
            ))
            print("Total \033[36m%s\033[0m (\033[35m%.2f ps\033[0m)" % (
                self.events_get,
                self.events_get / dif.seconds
            ))
            print(f"Taken \033[36m{dif}\033[0m")
            exit()

    async def _reactions_call(self) -> None:
        """
        Call every reaction
        """
        for reaction, payload in self.results:
            await reaction(self.event, payload)

    def _reactions_get(self) -> None:
        """
        Return list of needed funcs with payload
        """
        self.results = []
        for reaction in self.reactions[self.event.type]:
            payload = reaction.pl_gen(self.event) if reaction.pl_gen is not None else None

            for cond in reaction.conditions:
                if not cond.code(self.event, payload):
                    break
            else:
                self.results.append((reaction, payload))

    def _reactions_init(self) -> None:
        """
        Init reactions tree
        """
        reactions = {}

        for handler in self.reaction_handlers:
            if handler.event_name not in reactions:
                reactions[handler.event_name] = [handler.reaction]
            else:
                reactions[handler.event_name].append(handler.reaction)

        self.reactions = reactions

    def _failed_handler(self) -> Union[bool, None]:
        """
        Catch lp faileds
        """
        if 'failed' in self.lp:

            if self.lp['failed'] in self.faileds:
                self._failed_resolving()
                return True

            else:
                raise VkErr(str(self.lp))

        else:
            self.lp_info['ts'] = self.lp['ts']

    def _failed_resolving(self) -> None:
        """
        Resolve faileds problems
        """
        if self.lp['failed'] == 1:
            self.lp_info['ts'] = self.lp['ts']

        elif self.lp['failed'] in (2, 3):
            self.lp_info = self.auth(
                    self._method_name(),
                    self.start_settings
                )

        elif self.lp['failed'] == 4:
            self.lp_settings['version'] = self.lp['max_version']

    def _method_name(self) -> None:
        """
        Choose method for users and groups
        """
        if self.api.type == 'group':
            return 'groups.getLongPollServer'
        else:
            return 'messages.getLongPollServer'


class ReactionHandler:
    """
    Reactions Handler
    """
    def __init__(self, event_name) -> None:
        self.event_name = event_name

    def __call__(self, pl_gen=None):
        """
        Take payload generator
        """
        self.pl_gen = pl_gen

        self.__class__.__call__, self.__class__._reaction_decor =\
        self.__class__._reaction_decor, self.__class__.__call__

        return self

    def _reaction_decor(self, func: Any) -> Any:
        """
        Called when it is decorating
        """
        self.__class__.__call__, self.__class__._reaction_decor =\
        self.__class__._reaction_decor, self.__class__.__call__
        self.reaction = func

        func.event_name = self.event_name
        func.conditions = []
        func.pl_gen = self.pl_gen

        return func

class Keyboard:
    """
    Create VK Keyboard by dict or buttons list
    """
    def __init__(self, kb: Optional[dict] = None, **kwargs) -> None:
        if kb is None:
            self.kb = {
                **kwargs,
                'buttons': [[]]
            }
        else:
            self.kb = kb

    def __add__(self, button) -> None:
        """
        Add button to line
        """

        self.kb['buttons'][-1].append(button())

    def __repr__(self) -> str:
        """
        Create for sending
        """
        kb = json.dumps(self.kb, ensure_ascii=False)
        kb = kb.encode('utf-8').decode('utf-8')
        return str(kb)

    def create(self, *buttons):
        """
        Create keyboard by Buttons object
        """
        for button in buttons:
            if not isinstance(button, Button):
                raise TypeError(f"Keyboard's buttons must be 'Button' instance, not '{type(button).__name__}'")

            if button.info is None:
                self.kb['buttons'].append([])
            else:
                self.kb['buttons'][-1].append(button.info)

        return self


class Button:
    """
    Keyboard button
    """
    def __init__(self, **kwargs):
        self.info = {'action': {**kwargs}}

    def positive(self):
        """
        Green button
        """
        self.info['color'] = 'positive'
        return self

    def negative(self):
        """
        Red button
        """
        self.info['color'] = 'negative'
        return self

    def secondary(self):
        """
        White button
        """
        self.info['color'] = 'secondary'
        return self

    def primary(self):
        """
        Blue button
        """
        self.info['color'] = 'primary'
        return self

    @classmethod
    def _button_init(cls, **kwargs):
        self = super().__new__(cls)
        self.__init__(**kwargs)

        return self

    @classmethod
    def line(cls):
        """
        Add Buttons line
        """
        self = cls._button_init()
        self.info = None

        return self

    @classmethod
    def text(cls, **kwargs):
        return cls._button_init(type='text', **kwargs)

    @classmethod
    def open_link(cls, **kwargs):
        return cls._button_init(type='open_link', **kwargs)

    @classmethod
    def location(cls, **kwargs):
        return cls._button_init(type='location', **kwargs)

    @classmethod
    def vkpay(cls, **kwargs):
        return cls._button_init(type='vkpay', **kwargs)

    @classmethod
    def open_app(cls, **kwargs):
        return cls._button_init(type='open_app', **kwargs)
