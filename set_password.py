#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys, getopt
import os

def setSSID(new_ssid):
    os.system("adb shell \"sed -i 's/^ssid=.*/ssid=%s/g' data/misc/wifi/hostapd.conf\"" % new_ssid)

def setPass(new_pass):
    os.system("adb shell \"sed -i 's/wpa_passphrase=.*/wpa_passphrase=%s/g' data/misc/wifi/hostapd.conf\"" % new_pass)

def printSSIDPass():
    os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep ^ssid= | sed 's/ssid=/SSID：/g'\"")
    os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep wpa_passphrase= | sed 's/wpa_passphrase=/Password：/g'\"")

def setSuccessReboot():
    print ("更改成功,正在重启……")
    os.system("adb reboot -f")

def setFailed():
    print ("运行失败,-h 查看帮助文档")

def getInfo():
        print ("飞机信息：")
        printSSIDPass()
        os.system("adb shell \"getprop zz.product.version\"")
        os.system("adb shell \"opkg info | grep Version: | sed 's/Version:/IPK：/g'\"")

def getHelp():
    print("设置SSID：-s new_ssid 或 --sSSID new_ssid 或 --sSSID=new_ssid\n"
          "设置密码：-p new_pass 或 --sPASS new_password 或 --sPASS=new_password\n"
          "获取飞机信息：-g 或 --gINFO\n"
          "帮助文档：-h 或 --help")
set_ok = 0 # 定义返回设置/获取状态参数，判断是否设置/获取成功、是否需要重启
opts,args = getopt.gnu_getopt(sys.argv[1:],'-s:-p:-g-h',['sSSID=','sPASS=','gINFO','help'])

# 输入有冗余判断（只判断冗余的普通字符串，输入“-/--”开头的，getopt自身会判断并报错）
if args:
    setFailed()
    exit()

for opt_name,opt_values in opts:

    if opt_name in ('-s','--sSSID'):
        newSSID = opt_values
        setSSID(newSSID)
        set_ok += 4
    if opt_name in ('-p','--sPASS'):
        newPASS = opt_values
        setPass(newPASS)
        set_ok += 4
    if opt_name in ('-g', '--gINFO'):
        getInfo()
        set_ok += 1
    if opt_name in ('-h', '--help'):
        getHelp()
        set_ok += 1
print(set_ok)

# 判断是否设置/获取成功并要重启
if set_ok > 3:
    printSSIDPass()
    setSuccessReboot()
elif set_ok > 0:
    print ("获取成功")
else:
    setFailed() # 未输入命令行参数

# ssid=Hover_2-C2BD66