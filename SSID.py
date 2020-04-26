#coding=utf8
import os
# device = os.popen("adb devices").read()
# print(device)
# os.system("adb devices")

# password = os.popen("adb shell grep wpa_passphrase= data/misc/wifi/hostapd.conf").read()
# print (password)
os.system("adb shell grep wpa_passphrase= data/misc/wifi/hostapd.conf")


# ssid = os.popen("adb shell grep -E \"^ssid=\" data/misc/wifi/hostapd.conf").read()
# print(ssid)
os.system("adb shell grep -E \"^ssid=\" data/misc/wifi/hostapd.conf")
