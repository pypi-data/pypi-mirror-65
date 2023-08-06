#-*-coding:utf-8 -*-
import json
import os
import random
import subprocess
import time
from selenium import webdriver
from appium import webdriver as appiumServer

def udid(platformName="android"):
    if platformName == "android":
        return [i.split("\t")[0].strip() for i in os.popen("adb" + "  devices").readlines() if
         "device" in i and "attached" not in i]
    elif platformName == "ios":
        return os.popen("instruments -s devices").read().split("\n")



class Driver(object):
    def __init__(self,browser=None,executable_path_dict=None,appconfig=None):
        self.executable_path_dict = executable_path_dict
        # self.udid = udid
        # self.app_path = app
        if browser == "chrome":
            self.driver = webdriver.Chrome(executable_path=self.executable_path_dict["chromedriver"])
        elif browser == "safri":
            self.driver = webdriver.Safari()
        elif browser == "edge":
            self.driver = webdriver.Ie(executable_path=self.executable_path_dict["iedriver"])
        elif browser == "firefox":
            self.driver = webdriver.Firefox(executable_path=self.executable_path_dict["firefoxdriver"])
        elif browser == "edge":
            self.driver = webdriver.Firefox(executable_path=self.executable_path_dict["edgedriver"])
        elif browser == "android":
            self.udid = appconfig["udid"]
            self.app = appconfig["app"]
            self.port,self.bp = self.productrandom()
            caps = self.android_caps(appconfig)
            self.pid = self.AppiumServer()
            url = 'http://127.0.0.1:%s/wd/hub' % (self.port)
            self.driver = appiumServer.Remote(url,caps)

        elif browser == "ios":
            self.port, self.bp = self.productrandom()
            caps = self.iOS_caps(appconfig)
            self.udid  = appconfig["udid"]
            self.pid = self.AppiumServer()
            url = 'http://127.0.0.1:%s/wd/hub' % (self.port)
            self.driver = appiumServer.Remote(url, caps)

    def productrandom(self):
        port = random.randint(1111, 5555)
        bp = random.randint(11111, 33333)
        return port,bp

    def isPort(self):
        if os.name == "posix":
            pid = os.popen("lsof -i:%s|grep node|awk '{print $2}'" % str(self.port)).read()
        elif os.name == "nt":
            pid = os.popen("netstat -ano|findStr %s" % str(self.port)).read()[-8:].strip()
        if len(pid) != 0:
            return True
    
    def kill_appiumServer(self,pid):
        pid.kill()
        
    def AppiumServer(self):
        try:
            if "appium_server_path" in self.executable_path_dict.keys():
                appium_server_path = self.executable_path_dict["appium_server_path"]
            else:
                appium_server_path = "appium"
        except:
            appium_server_path = "appium"

        # port,bp = self.productrandom()
        cmd = appium_server_path+" -a 127.0.0.1 -U %s -p %s -bp %s --command-timeout 100000 --session-override" % (self.udid, self.port, self.bp)
        # url = 'http://127.0.0.1:%s/wd/hub' % (port)
        pid = subprocess.Popen(cmd, shell=True)
        print("正在启动appium服务，请稍等.....")
        n = 0
        while True:
            isPort = self.isPort()
            if isPort == True:
                 break
            else:
                time.sleep(5)
                n+=1
            if n > 5:

                raise RuntimeError("appium server is error, please reconnect appiumse!!!")
        print("成功启动appium服务，请稍等.....")
        return pid


    def android_caps( self, appconfig, isApp=False, isResetKeyboard=False):
        if "adb_path" in appconfig.keys():
            adb_path = self.executable_path_dict["adb_path"]
        else:
            adb_path = "adb"
        if "aapt_path" in appconfig.keys():
            aapt_path = self.executable_path_dict["aapt_path"]
        else:
            aapt_path = "aapt"

        if os.name == "posix":
            aapt_dump = "%s dump badging %s |grep %s|awk '{print $2}'"
            appPackage = str(os.popen(aapt_dump % (aapt_path,appconfig["app"], "package")).read()).strip()[6:-1]
            # print(aapt_dump % (aapt_path,app_path, "launchable-activity"))
            try:
                appActivity = str(
                    os.popen(aapt_dump % (aapt_path,appconfig["app"], "launchable-activity")).read()).split()[
                                  0].strip()[6:-1]
            except Exception as e:
                appActivity = appPackage + ".main.MainActivity"

        elif os.name == "nt":
            appPackage = os.popen('%s dump badging  %s |findStr "package:" ' % (aapt_path,appconfig["app"])).read().split(" ")[
                             1].strip()[6:-1]
            try:
                appActivity = \
                os.popen('%s dump badging %s |findStr "launchable-activity"' % (aapt_path,appconfig["app"])).read().split(" ")[
                    1].strip()[
                6:-1]
            except:
                appActivity = appPackage + ".main.MainActivity"

            # udids = str(os.popen("%s devices|grep -v devices|awk '{print $1}'" % (self.adb_path)).read()).split("\n")
            # udids = list(filter(None, udids))
        android_version = os.popen(
            "%s -s %s shell getprop ro.build.version.release" % (adb_path, self.udid)).read().strip()
        print("%s -s %s shell getprop ro.product.name" % (adb_path, self.udid))
        android_name = os.popen("%s -s %s shell getprop ro.product.name" % (adb_path, self.udid)).read().strip()
        if int(android_version[0]) <= 4:
            error = "Android Version must be greater than 4 !"
            raise RuntimeError(error)

        caps = {"platformName": "android",
                "platformVersion": android_version,
                "app": appconfig["app"],
                "udid": self.udid,
                # "newCommandTimeout":100000,
                "deviceName": android_name,
                "appPackage": appPackage,
                "appActivity": appActivity}
        if isResetKeyboard == True:
            caps.update({'unicodeKeyboard': True,
                         'resetKeyboard': True})
        if isApp == True:
            caps.update({"noReset": True})
        print("caps ----->",caps)
        # print(json.loads(caps))
        return caps


    def iOS_caps(self,caps):
        capability = {
            "platformName":"iOS",
            "automationName":"XCUITest",
            # "platformVersion":caps["deviceName"],
            # "deviceName":caps["deviceName"],
            # "udid":caps["udid"],
            # "bundleid":caps["bundleid"],
        }
        capability.update(caps)
        return capability

if __name__ == '__main__':
    #config
    executable_path_dict = {"adb_path": "/Users/zhenghong/Library/Android/sdk/platform-tools/adb",
                            "aapt_path": "/Users/zhenghong/Library/Android/sdk/build-tools/29.0.3/aapt",
                            "firefoxdriver": "/Users/zhenghong/work/gitee/AutomationFramework/conf/geckodriver",
                            "chromedriver": "/Users/zhenghong/work/gitee/AutomationFramework/conf/chromedriver"
                            ,"appium_server_path":"appium"
                            }
    udid = "c466fa9e"
    app = "/Users/zhenghong/Downloads/5c47c901156bc90525eb486b9095c12a.apk"
    # Driver(browser="android",udid=udid,app=app,executable_path_dict=executable_path_dict)
    #
    # Driver(browser="android",udid=udid,app=app,executable_path_dict=executable_path_dict)

    # driver = Driver("chrome",executable_path_dict=executable_path_dict).driver #启动Chrome浏览器
    # driver = Driver("safri",executable_path_dict=executable_path_dict).driver #启动safri浏览器
    # driver = Driver("firefox",executable_path_dict=executable_path_dict).driver #启动firefox浏览器

