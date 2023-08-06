import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vk_dev",
    version="2.1.3",
    author="Yan",
    author_email="deknowny@gmail.com",
    description="Package for creating VK bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rhinik/vk_bot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['aiohttp==3.6.2', 'requests==2.23.0'],
    python_requires='>=3.6',
)
