#-*-coding:utf-8 -*-

import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UI-Automation-Framework",
    version="0.1.6.1",
    author="lzh",
    author_email="743872668@qq.com",
    description="UI自动化框架，集成APPIUM、selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chenzheng102/UI-Automation-Framework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)