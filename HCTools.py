#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/5/6
# @Author  : ShuHan Ji
# @File    : HCTools.py
# @Software: vscode
import sys, getopt
import os
import wget, zipfile, glob, time, shutil

def setSSID(new_ssid):
    os.system("adb shell \"sed -i 's/^ssid=.*/ssid=%s/g' data/misc/wifi/hostapd.conf\"" % new_ssid)

def setPass(new_pass):
    os.system("adb shell \"sed -i 's/wpa_passphrase=.*/wpa_passphrase=%s/g' data/misc/wifi/hostapd.conf\"" % new_pass)

def setBand(new_band):
    os.system("adb shell \"sed -i 's/hw_mode=.*/hw_mode=%s/g' data/misc/wifi/hostapd.conf\"" % new_band)

def printSSIDPass():
    os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep ^ssid= | sed 's/ssid=/SSID：/g'\"")
    os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep wpa_passphrase= | sed 's/wpa_passphrase=/Password：/g'\"")

def setSuccessReboot():
    print ("更改成功,正在重启……")
    os.system("adb reboot -f")

def setFailed():
    softMessage()
    print ("\n运行失败，查看帮助文档:\npython HCTools.py -h")

# 下载天空端最新zip
def downloadLatestSky(branch_name):
    SkyUrlHead="http://ci.zerozero.cn:88/view/6.HC2_BRemoter/job/HC2_BRemoter-"
    SkyUrlTail="/lastSuccessfulBuild/artifact/*zip*/downLoadSky.zip"
    urlAll = '%s%s%s' % (SkyUrlHead, newBranch, SkyUrlTail)
    wget.download(urlAll, out=None, bar=None)

def updateSky(branch_name):
    """升级天空端"""
    if defineImageMode():
        downloadLatestSky(branch_name)
        sky_file_name =unzip_file('./downLoadSky.zip','./downLoadSky')
        print('图传模式')
        sky_file_path = "".join(glob.glob(r'./downLoadSky/archive/ota_sky*')) #  模糊匹配,获取文件路径并转化为字符串
        sky_file_name = sky_file_path.split('/')[-1] # 从地址中提取文件名
        print(sky_file_name)
        updateSkyToDrone(sky_file_path, sky_file_name)
        deleteZipDir('./downLoadSky.zip','./downLoadSky')
    else:
        print('升级失败，请将飞机切换到图传模式!')


def unzip_file(zip_src, dst_dir):
    """解压zip文件夹（文件名，文件地址）"""
    file = zipfile.ZipFile(zip_src, 'r')
    file.extractall(dst_dir)
    

def defineImageMode():
    """确认是否为图传模式"""
    image_band = os.popen("adb shell lsusb").read()
    if('aaaa:aa97' in image_band):
        return 1
    else:
        return 0

def updateSkyToDrone(file_path, file_name):
    """push天空端安装包并执行升级脚本"""
    os.system("adb push %s /hover/tests/fpv/" % file_path)
    os.system("adb shell systemctl stop zz_fpv")
    time.sleep(0.1)
    os.system("adb shell \"/hover/tests/fpv/fpv_upgrade /hover/tests/fpv/%s\"" % file_name)
    print('\n安装包:', file_name, '\n安装完成！')


def deleteZipDir(zip_path, dir_path):
    """删除本地下载的安装包zip和解压的文件夹"""
    os.remove(zip_path)
    shutil.rmtree(dir_path)

def getWiFi():
    wifi_band_mark = os.popen("adb shell \"cat data/misc/wifi/hostapd.conf | grep hw_mode= | sed 's/hw_mode=//g'\"").read().strip('\n')
    if wifi_band_mark == "a":
        wifi_band = "5G"
    elif wifi_band_mark =="g":
        wifi_band = "2.4G"
    print ("Wi-Fi:",wifi_band)

def getInfo():
        print ("飞机信息：")
        printSSIDPass()
        getWiFi()
        os.system("adb shell \"getprop zz.product.version\"")
        os.system("adb shell \"opkg info | grep Version: | sed 's/Version:/IPK：/g'\"")

def getHelp():
    softMessage()
    print("     设置SSID：-s new_ssid 或 --sSSID new_ssid 或 --sSSID=new_ssid\n"
          "     设置密码：-p new_pass 或 --sPASS new_password 或 --sPASS=new_password\n"
          "切换Wi-Fi频段：-w 5(5g/5G) 或 -w 2(2g/2G/2.4/2.4g/2.4G) 或 --sWIFI new_band\n"
          "   升级天空端：-k totest(dev) 或 --uSKY totset(dev)\n"
          " 获取飞机信息：-g 或 --gINFO\n"
          "     帮助文档：-h 或 --help")


def softMessage():
    print ("------------------------------------------------------------------")
    print ("HCTools")
    print ()
    print ("e-mail: jishuhan@zerozero.cn")
    print ("version: 1.0.0")
    print ("------------------------------------------------------------------")
    print ()

set_ok = 0 # 定义返回设置/获取状态参数，判断是否设置/获取成功、是否需要重启
opts,args = getopt.gnu_getopt(sys.argv[1:],'-s:-p:-w:-k:-g-h',['sSSID=','sPASS=','sWIFI=','uSKY=','gINFO','help'])

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
    if opt_name in ('-w','--sWIFI'):
        newBand = opt_values
        if newBand in ('5','5g','5G'):
            newBand = 'a'
        elif newBand in ('2','2g','2G','2.4','2.4g','2.4G'):
            newBand = 'g'
        setBand(newBand)
        set_ok += 4
    if opt_name in ('-k','--uSKY'):
        newBranch = opt_values
        if newBranch in ('dev','develop','DEV','Dev'):
            newBranch = 'Dev'
        elif newBranch in ('totest','Totest','ToTest','toTest'):
            newBranch = 'To-Test'
        else:
            setFailed()
            exit
        updateSky(newBranch)
        set_ok += 1
    if opt_name in ('-g', '--gINFO'):
        getInfo()
        set_ok += 1
    if opt_name in ('-h', '--help'):
        getHelp()
        set_ok += 1

# 判断是否设置/获取成功并要重启
if set_ok > 3:
    printSSIDPass()
    getWiFi()
    setSuccessReboot()
elif set_ok == 0:
    setFailed() # 未输入命令行参数

# ssid=Hover_2-C2BD66