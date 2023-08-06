#-*- utf-8 -*-

#get devices
import os
def udid(platformName="android"):
    if platformName == "android":
        return [i.split("\t")[0].strip() for i in os.popen("adb" + "  devices").readlines() if
         "device" in i and "attached" not in i]

    elif platformName == "ios":
        return os.popen("instruments -s devices").read().split("\n")



