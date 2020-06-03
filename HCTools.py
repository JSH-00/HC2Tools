#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/5/6
# @Author  : ShuHan Ji
# @File    : HCTools.py
# @Software: vscode
import sys, getopt
import os
import wget, zipfile, glob, time, shutil, urllib.request, tarfile
import getpass
CACHE_PATH = os.path.join(os.path.expanduser("~"), 'Library')
CACHE_PATH_FILE = CACHE_PATH + '/HCTool_temp'
def setSSID(new_ssid):
    os.system("adb shell \"sed -i 's/^ssid=.*/ssid=%s/g' data/misc/wifi/hostapd.conf\"" % new_ssid)

def setPass(new_pass):
    os.system("adb shell \"sed -i 's/wpa_passphrase=.*/wpa_passphrase=%s/g' data/misc/wifi/hostapd.conf\"" % new_pass)

def setBand(new_band):
    os.system("adb shell \"sed -i 's/hw_mode=.*/hw_mode=%s/g' data/misc/wifi/hostapd.conf\"" % new_band)

def printSSIDPass():
    os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep ^ssid= | sed 's/ssid=/SSID：/g'\"")
    os.system("adb shell \"cat data/misc/wifi/hostapd.conf | grep wpa_passphrase= | sed 's/wpa_passphrase=/Password：/g'\"")

def isReboot(reboot_number):
    """判断是否要重启"""
    if reboot_number > 99:
        reboot_event = '升级'
    elif set_ok > 3:
        reboot_event = '更改'
    elif set_ok >0:
        exit()
    elif set_ok == 0:
        setFailed('未传入参数') # 未输入命令行参数
        exit()
    print ("------------------------------------------------------------------")
    getInfo()
    os.system("adb reboot -f")
    print ("------------------------------------------------------------------")
    print ("%s完成,正在重启……" % reboot_event)

def cachePathExist():
    """判断缓存目录是否存在，不存在则新建文件夹"""
    if os.path.exists(CACHE_PATH_FILE):
        return 1
    else:
        print('新建缓存目录' + CACHE_PATH_FILE)
        os.makedirs(CACHE_PATH_FILE)

def setFailed(fail_name):
    softMessage()
    print ("%s，运行失败，查看帮助文档:\npython3 HCTools.py -h\n\n" % fail_name)

def downloadLatestSky(branch_name):
    """下载天空端最新zip"""
    SkyUrlHead="http://ci.zerozero.cn:88/view/6.HC2_BRemoter/job/HC2_BRemoter-"
    SkyUrlTail="/lastSuccessfulBuild/artifact/*zip*/downLoadSky.zip"
    urlAll = '%s%s%s' % (SkyUrlHead, branch_name, SkyUrlTail)
    wget.download(urlAll, out=None, bar=None)

def updateSky(input_name):
    if isNotImageMode():
        print('升级失败，请将飞机切换到图传模式!')
        exit()
    if input_name in ('dev','develop','DEV','Dev'):
        updateSkyURL('Dev')
    elif input_name in ('totest','Totest','ToTest','toTest'):
        updateSkyURL('To-Test')
    elif os.path.exists('./' + input_name):
        updateSkyLocal(input_name)
    else:
        setFailed('参数错误')
        exit()

def updateSkyURL(branch_name):
    """升级天空端（使用分支最新安装包）"""
    downloadLatestSky(branch_name)
    sky_file_name = unzip_file('./downLoadSky.zip','./downLoadSky')
    sky_file_path = "".join(glob.glob(r'./downLoadSky/archive/ota_sky*')) # 模糊匹配,获取文件路径并转化为字符串
    sky_file_name = sky_file_path.split('/')[-1] # 从地址中提取文件名
    updateSkyToDrone(sky_file_path, sky_file_name, branch_name)
    deleteZipDir('./downLoadSky.zip', './downLoadSky')

def updateSkyLocal(sky_file_name):
    """升级天空端（使用本地安装包）"""
    updateSkyToDrone('./' + sky_file_name, sky_file_name, '本地')

def unzip_file(zip_src, dst_dir):
    """解压zip文件夹（文件名，文件地址）"""
    file = zipfile.ZipFile(zip_src, 'r')
    file.extractall(dst_dir)
    
def untar_file(file_name, file_path):
    """解压tar或tar.gz文件夹(文件名，缓存总目录地址）"""
    dir_path = CACHE_PATH_FILE + '/'+ file_name # 对应的解压文件夹路径
    tar = tarfile.open(dir_path + '.tar.gz') #对应的解压包路径
    names = tar.getnames()
    if os.path.isdir(dir_path):
        pass
    else:
        os.mkdir(dir_path)
    #由于解压后是许多文件，预先建立同名文件夹
    for name in names:
        tar.extract(name, dir_path)

def isNotImageMode():
    """确认是否为图传模式"""
    image_band = os.popen("adb shell lsusb").read()
    if('aaaa:aa97' in image_band):
        return 0 # 图传
    else:
        return 1 # 非图传

def updateSkyToDrone(file_path, file_name, file_place):
    """push天空端安装包并执行升级脚本"""
    os.system("adb push %s /hover/tests/fpv/" % file_path)
    os.system("adb shell systemctl stop zz_fpv")
    time.sleep(0.1)
    os.system("adb shell \"/hover/tests/fpv/fpv_upgrade /hover/tests/fpv/%s\"" % file_name)
    print('\n%s安装包:' % file_place, file_name)

def deleteZipDir(zip_path, dir_path):
    """删除本地下载的安装包zip和解压的文件夹"""
    os.remove(zip_path)
    shutil.rmtree(dir_path)

def updateIpk(branch_name):
    """升级IPK某分支最新包"""
    if branch_name in ('Dev', 'dev'):
        branch_name = 'Dev'
        # ci最新build成功的版本号
        build_numble = urllib.request.urlopen("http://ci.zerozero.cn:88/job/3.HC2Repo-Dev/lastSuccessfulBuild/buildNumber").read().decode('utf-8')
        url_numble = 3
        ipk_file_name = 'HC2_%s.release_%s' % (branch_name, build_numble) # 没有后缀的Dev文件名
    elif branch_name in ('ToTest', 'totest'):
        branch_name = 'ToTest'
        build_numble = urllib.request.urlopen("http://ci.zerozero.cn:88/job/2.HC2Repo-ToTest/lastSuccessfulBuild/buildNumber").read().decode('utf-8')
        url_numble = 2
        ipk_file_name = ('HC2Repo-%s.release_%s' % (branch_name, build_numble)) # 没有后缀的ToTest文件名
    else:
        setFailed('参数错误')
        exit()
    downloadIpk(url_numble, branch_name, build_numble, ipk_file_name)

def  downloadIpk(url_numble, branch_name, build_numble, ipk_file_name):
    """下载IPK最新tar.gz解压并安装"""
    cachePathExist() # 判断缓存文件夹是否存在
    urlAll = ('http://ci.zerozero.cn:88/job/%s.HC2Repo-%s/lastSuccessfulBuild/artifact/%s.tar.gz' % (url_numble, branch_name, ipk_file_name))
    ipk_untar_path = CACHE_PATH_FILE + '/' + ipk_file_name # 解压后文件夹路径
    ipk_file_path = ipk_untar_path + '.tar.gz' # 未解压ipk文件路径
    if not os.path.exists(ipk_file_path):
        print(ipk_file_name + '.tar.gz 下载中...')
        urllib.request.urlretrieve(urlAll, CACHE_PATH_FILE + '/' + ipk_file_name + '.tar.gz', callbackfunc)
        print('下载完成，正在解压文件并升级...')
        untar_file(ipk_file_name, CACHE_PATH_FILE)
    elif not os.path.exists(ipk_untar_path):
        untar_file(ipk_file_name, CACHE_PATH_FILE)
        print('文件已存在，正在解压文件并升级...')
    else:
        print('文件已存在，正在升级...')
    os.chdir(ipk_untar_path) # 进入文件夹
    os.system('./install.sh') # 执行安装脚本

def callbackfunc(blocknum, blocksize, totalsize):
    '''下载进度条
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    sys.stdout.write("  %.2f%%\r" % percent)        
    sys.stdout.flush()

def getWiFi():
    wifi_band_mark = os.popen("adb shell \"cat data/misc/wifi/hostapd.conf | grep hw_mode= | sed 's/hw_mode=//g'\"").read().strip('\n')
    if wifi_band_mark == "a":
        wifi_band = "5G"
    elif wifi_band_mark =="g":
        wifi_band = "2.4G"
    print ("Wi-Fi:", wifi_band)

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
          "     升级IPK：-i totest(dev) 或 --uIPK totset(dev)\n"
          "   升级天空端：-k totest(dev/本地安装包名) 或 --uSKY totset(dev/本地安装包名)\n"
          " 获取飞机信息：-g 或 --gINFO\n"
          "     帮助文档：-h 或 --help\n")

def softMessage():
    print ("------------------------------------------------------------------")
    print ("HCTools")
    print ()
    print ("e-mail: jishuhan@zerozero.cn")
    print ("version: 1.0.0")
    print ("------------------------------------------------------------------")
    print ()

set_ok = 0 # 定义返回设置/获取状态参数，判断是否设置/获取成功、是否需要重启
opts,args = getopt.gnu_getopt(sys.argv[1:],'-s:-p:-w:-k:-i:-g-h',['sSSID=','sPASS=','sWIFI=','uSKY=','uIPK=','gINFO','help'])

# 输入有冗余判断（只判断冗余的普通字符串，输入“-/--”开头的，getopt自身会判断并报错）
if args:
    setFailed('参数错误')
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
        skyValue = opt_values
        updateSky(skyValue)
        set_ok += 100
    if opt_name in ('-i','--uIPK'):
        ipkValue = opt_values
        updateIpk(ipkValue)
        set_ok += 100
    if opt_name in ('-g', '--gINFO'):
        getInfo()
        set_ok += 1
    if opt_name in ('-h', '--help'):
        getHelp()
        set_ok += 1
isReboot(set_ok) # 判断是否升级/设置/获取成功并要重启