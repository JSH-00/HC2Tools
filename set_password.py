#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys, getopt
import os

def setPassSSID(arg_pass, arg_ssid):
    setPass(arg_pass)
    setSSID(arg_ssid)

def setSSIDPass(arg_ssid, arg_pass):
    setSSID(arg_ssid)
    setPass(arg_pass)

def setSuccess():
    print ("更改成功!!")
    os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep ^ssid= | sed 's/ssid=/SSID：/g'\"")
    os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep wpa_passphrase= | sed 's/wpa_passphrase=/Password：/g'\"")
    os.system("adb reboot -f")

def setPass(arg_pass):
    os.system("adb shell \"sed -i 's/wpa_passphrase=.*/wpa_passphrase=%s/g' data/misc/wifi/hostapd.conf\"" % arg_pass)

def setSSID(arg_ssid):
    os.system("adb shell \"sed -i 's/^ssid=.*/ssid=%s/g' data/misc/wifi/hostapd.conf\"" % arg_ssid)

def getHelp():
    print("设置SSID和密码：python XXX.py -sSSID new_ssid -sPASS new_password")
    print("设置密码和SSID：python XXX.py -sPASS new_password -sSSID new_ssid")
    print("设置SSID：python XXX.py -sSSID new_ssid")
    print("设置密码：python XXX.py -sPASS new_password")
    print("获取飞机信息：python XXX.py -g")
    print("帮助文档：python XXX.py -h")

if  sys.argv[1] == "-sSSID" and sys.argv[3] == "-sPASS":
    setPassSSID(sys.argv[2], sys.argv[4])
    setSuccess()
elif sys.argv[1] == "-sPASS" and sys.argv[3] == "-sSSID":
    setSSIDPass(sys.argv[2], sys.argv[4])
    setSuccess()
elif sys.argv[1] == "-sPASS":
    setPass(sys.argv)
    setSuccess()
elif sys.argv[1] == "-sSSID":
    setPass(sys.argv)
    setSuccess()
elif sys.argv[1] == "-g":
    print ("飞机信息：")
    os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep ^ssid= | sed 's/ssid=/SSID：/g'\"")
    os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep wpa_passphrase= | sed 's/wpa_passphrase=/Password：/g'\"")
    os.system("adb shell \"getprop zz.product.version\"")
    os.system("adb shell \"opkg info | grep Version: | sed 's/Version:/IPK：/g'\"")
elif sys.argv[1] == "-h":
    getHelp()
else:
    print ("运行失败,-h 查看帮助文档")

# os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep ^ssid=\"")
# os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep wpa_passphrase=\"")
# os.system("adb shell \"sed -i 's/^ssid=.*/ssid=Hover_JSH/g' data/misc/wifi/hostapd.conf\"")
# os.system("adb shell \"sed -i 's/wpa_passphrase=.*/wpa_passphrase=0987654321/g' data/misc/wifi/hostapd.conf\"")
# os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep ^ssid=\"")
# os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep wpa_passphrase=\"")

# ssid=Hover_2-C2BD66