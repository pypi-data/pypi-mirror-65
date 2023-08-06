import os

from UIAutomationFramework.common.UiAutoDriver import Driver
path = os.path.abspath("../apps/ApiDemos-debug.apk")
appconfig = {"app":path,
             "udid":"c466fa9e"}
Driver(browser="android", appconfig=appconfig)
