UI Automation Framework
====================

[![PyPI version](https://badge.fury.io/py/UI-Automation-Framework.svg)](https://badge.fury.io/py/UI-Automation-Framework)
[![Downloads](https://pepy.tech/badge/UI-Automation-Framework)](https://pepy.tech/project/UI-Automation-Framework)

<!-- [![Build Status](https://travis-ci.org/appium/python-client.svg?branch=master)](https://travis-ci.org/appium/python-client) -->
<!-- [![Build Status](https://dev.azure.com/ki4070ma/python-client/_apis/build/status/appium.python-client?branchName=master)](https://dev.azure.com/ki4070ma/python-client/_build/latest?definitionId=2&branchName=master) -->


In order to uniformly use the webdriver of one startup class, an extension library encapsulates a class in two libraries, namely selenium and appium-python-client. After configuring the corresponding parameters, webdriver can be started
    [Selenium 3.0 draft](https://dvcs.w3.org/hg/webdriver/raw-file/tip/webdriver-spec.html)
    [Mobile JSON Wire Protocol Specification draft](https://github.com/SeleniumHQ/mobile-spec/blob/master/spec-draft.md)
    [Appium](https://appium.io).
    [selenium](https://www.selenium.dev/)


#version history

    ```shell
    version 0.1.1
    新增装饰器check_error

    version 0.1.2
    优化appium 启动Android相关代码

    version 0.1.4
    新增appium 启动iOS配置相关代码
    提供获取设备udid _apis

    v0.1.5
    优化代码结构，支持iOS自动化测试

    v0.1.6
    更新README.md文档
    ```

# Getting the UI Automation Framework

There are three ways to install and use the UI Automation Framework.

1. Install from [PyPi](https://pypi.org), as
['UI-Automation-Framework'](https://pypi.org/project/UI-Automation-Framework/).
    ```shell
    pip install Appium-Python-Client
    pip install selenium
    pip install UIAutomationFramework

    ```

    You can see the history from [here](https://pypi.org/project/UI-Automation-Framework/#history)

2. Install from source, via [PyPi](https://pypi.org). From ['UI-Automation-Framework'](https://pypi.org/project/UI-Automation-Framework/),
download and unarchive the source tarball (UI-Automation-Framework-X.X.tar.gz).

    ```shell
    tar -xvf UI-Automation-Framework-X.X.tar.gz
    cd UI-Automation-Framework-X.X
    python setup.py install
    ```

4. mac Environment configuration

    ```shell
    第一步：配置 .bash_profile文件
    vim ~/.bash_profile
    JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-13.0.1.jdk/Contents/Home
    CLASSPAHT=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
    ANDROID_HOME=/Users/zhenghong/Library/Android/sdk
    export PATH=${PATH}:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/emulator:${ANDROID_HOME}/tools:${ANDROID_HOME}/build-tools/29.0.3
    PATH=${JAVA_HOME}/bin:$PATH:
    export JAVA_HOME
    export CLASSPATH
    export PATH
    source ~/.bash_profile

    第二步：
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    brew install node
    npm install -g  appium
    npm install -g  appium-doctor
    brew install libimobiledevice --HEAD
    brew install carthage
    npm install -g ios-deploy
    gem install xcpretty

    第三步：
    appium-doctor --ios 查询iOS环境
    appium-doctor --Android 查询Android环境

    ```
5. Window Environment configuration

    ```shell
    待更新
    ```