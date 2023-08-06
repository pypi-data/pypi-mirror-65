import os
import time
from random import randint

from UIAutomationFramework.common.UiAutoDriver import Driver
def startApp():
    app = os.path.abspath('../apps/TestApp-iphonesimulator.app')
    # command_executor = 'http://127.0.0.1:4723/wd/hub',
    desired_capabilities={
                    'app': app,
                    'platformName': 'iOS',
                    'platformVersion': '13.3',
                    'deviceName': 'iPhone 11'
                    ,"udid":"AB0E1D2C-1573-49E1-B116-3FE286D87D5B"
                }
    base = Driver(browser="ios",appconfig=desired_capabilities)
    driver = base.driver

    els = [driver.find_element_by_accessibility_id('TextField1'),
           driver.find_element_by_accessibility_id('TextField2')]

    _sum = 0
    for i in range(2):
        rnd = randint(0, 10)
        els[i].send_keys(rnd)
        _sum += rnd
    time.sleep(10)
    base.kill_appiumServer(base.pid)
startApp()

