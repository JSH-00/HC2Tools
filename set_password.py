#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys, getopt
import os
os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep ^ssid=\"")
os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep wpa_passphrase=\"")
if  sys.argv[1]=="-sSSID" and sys.argv[3]=="-sPASS":

    os.system("adb shell \"sed -i 's/^ssid=.*/ssid=%s/g' data/misc/wifi/hostapd.conf\""%(sys.argv[2]))
    os.system("adb shell \"sed -i 's/wpa_passphrase=.*/wpa_passphrase=%s/g' data/misc/wifi/hostapd.conf\""%(sys.argv[4]))
    os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep ^ssid=\"")
    os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep wpa_passphrase=\"")
    os.system("adb reboot -f")
    # print (len(sys.argv))

# os.system("python haha.py %s %s" % (paramA,paramB))

# os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep ^ssid=\"")
# os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep wpa_passphrase=\"")
# os.system("adb shell \"sed -i 's/^ssid=.*/ssid=Hover_JSH/g' data/misc/wifi/hostapd.conf\"")
# os.system("adb shell \"sed -i 's/wpa_passphrase=.*/wpa_passphrase=0987654321/g' data/misc/wifi/hostapd.conf\"")
# os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep ^ssid=\"")
# os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep wpa_passphrase=\"")

# ssid=Hover_2-C2BD66