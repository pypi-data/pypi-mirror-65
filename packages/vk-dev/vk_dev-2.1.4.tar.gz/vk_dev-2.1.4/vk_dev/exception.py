class VkErr(Exception):
    """
    Errors from response from vk
    """
    lp_faileds = {
        1: "The event history went out of date or was partially lost",
        2: "The key’s active period expired",
        3: "Information was lost",
        4: "Invalid version number was passed"
    }
    lp_handler_text = ". \033[33mYou can use auto LP faileds handler in LongPoll class\033[0m"
    def __init__(self, text):
        self.text = text

    @staticmethod
    def text_init(text):
        if isinstance(text, dict):
            if "failed" in text:
                return self.lp_faileds[text["failed"]] + self.lp_handler_text

            elif 'error' in text:

                head_msg = f"\n\033[31m[{text['error']['error_code']}] {text['error']['error_msg']}\033[0m\n"
                content = "Request params:"
                for pair in text["error"]["request_params"]:
                    content += f"\n\033[33m{pair['key']}\033[0m = \033[36m{pair['value']}\033[0m"
                return head_msg + content

            return text

        return text
