#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/5/6
# @Author  : ShuHan Ji
# @File    : HCTools.py
# @Software: vscode
import sys, getopt, os, zipfile, glob, time, shutil, urllib.request, tarfile, getpass
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

def getCacheFilePath(file_name):
    """返回文件缓存路径"""
    return CACHE_PATH_FILE + '/' + file_name

def createCachePathIfNeed():
    """判断缓存目录是否存在，不存在则新建文件夹"""
    if os.path.exists(CACHE_PATH_FILE):
        return 1
    else:
        print('新建缓存目录' + CACHE_PATH_FILE)
        os.makedirs(CACHE_PATH_FILE)

def setFailed(fail_name):
    softMessage()
    print ("%s，运行失败，查看帮助文档:\npython3 HCTools.py -h\n\n" % fail_name)

def downloadLatestBRemoter(branch_name):
    """下载天空端最新zip"""
    build_numble = urllib.request.urlopen("http://ci.zerozero.cn:88/view/6.HC2_BRemoter/job/HC2_BRemoter-%s/lastSuccessfulBuild/buildNumber" % branch_name).read().decode('utf-8')
    big_remoter_url = 'http://ci.zerozero.cn:88/view/6.HC2_BRemoter/job/HC2_BRemoter-' + branch_name + '/lastSuccessfulBuild/artifact/*zip*/downLoadSky.zip'
    unzip_folder_path = CACHE_PATH_FILE + '/BRemoter_' + branch_name + '_' + build_numble
    download_big_remoter_path = unzip_folder_path + '.zip'
    downloadUntarIfNeed(download_big_remoter_path, unzip_folder_path, big_remoter_url)
    return download_big_remoter_path, unzip_folder_path # 返回下载包、解压文件夹的绝对路径

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
    big_remoter_file_path, unzip_folder_path = downloadLatestBRemoter(branch_name)
    big_remoter_ota_sky_bin_path = "".join(glob.glob('%s/archive/ota_sky*' % unzip_folder_path)) # 模糊匹配,获取文件路径并转化为字符串
    ota_sky_bin_name = big_remoter_ota_sky_bin_path.split('/')[-1] # 从地址中提取文件名
    updateSkyToDrone(big_remoter_ota_sky_bin_path, ota_sky_bin_name, branch_name)

def updateSkyLocal(sky_file_name):
    """升级天空端（使用本地安装包）"""
    updateSkyToDrone('./' + sky_file_name, sky_file_name, '本地')

def unzip_file(zip_src, dst_dir):
    """解压zip文件夹（文件名，文件地址）"""
    file = zipfile.ZipFile(zip_src, 'r')
    file.extractall(dst_dir)
    
def untar_file(file_name, dir_path):
    """解压tar或tar.gz文件夹（文件缓存路径，文件夹缓存路径）"""
    tar = tarfile.open(file_name) #对应的解压包路径
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

def updateSkyToDrone(file_path, file_name, file_place_or_branch):
    """push天空端安装包并执行升级脚本(安装文件的路径，安装文件名，分支名)"""
    os.system("adb push %s /hover/tests/fpv/" % file_path)
    os.system("adb shell systemctl stop zz_fpv")
    time.sleep(0.1)
    os.system("adb shell \"/hover/tests/fpv/fpv_upgrade /hover/tests/fpv/%s\"" % file_name)
    print('\n%s安装包:' % file_place_or_branch, file_name)

def getIpkInfo(branch_name):
    """获取ipk分支最新文件名和URL"""
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
    download_ipk_url = ('http://ci.zerozero.cn:88/job/%s.HC2Repo-%s/lastSuccessfulBuild/artifact/%s.tar.gz' % (url_numble, branch_name, ipk_file_name))
    return ipk_file_name, download_ipk_url # 返回：文件名(不带后缀)、下载URL

def updateIpk(branch_name):
    """升级IPK某分支最新包"""
    createCachePathIfNeed() # 判断缓存文件夹是否存在
    ipk_file_name, download_ipk_url = getIpkInfo(branch_name)
    untar_folder_cache_path = getCacheFilePath(ipk_file_name) # 最新版IPK本地解压文件夹缓存路径
    download_ipk_cache_path = getCacheFilePath(ipk_file_name + '.tar.gz') # 最新版IPK本地缓存路径
    downloadUntarIfNeed(download_ipk_cache_path, untar_folder_cache_path, download_ipk_url)
    os.chdir(untar_folder_cache_path) # 进入文件夹
    os.system('./install.sh') # 执行安装脚本

def  downloadFromUrl(download_url, download_path):
    """下载URL的文件并保存到指定路径（下载URL，下载路径）"""
    urllib.request.urlretrieve(download_url, download_path, callbackfunc)

def downloadUntarIfNeed(download_file_path, untar_folder_path, download_file_url):
    """如果需要，则下载并解压（下载路径，解压文件夹路径，下载URL）"""
    if not os.path.exists(download_file_path):
        print(download_file_path + '\n下载中...')
        urllib.request.urlretrieve(download_file_url, download_file_path, callbackfunc)
        print('下载完成，正在解压...')
        unzipOrUntar(download_file_path, untar_folder_path)
    elif not os.path.exists(untar_folder_path):
        unzipOrUntar(download_file_path, untar_folder_path)
        print(download_file_path + '\n文件已存在，正在解压...')
    else:
        print(download_file_path + '\n文件已存在，准备升级...')

def unzipOrUntar(zip_file_path, file_unzip_folder_path):
    '''判断解压文件类型并解压到指定文件夹（压缩文件路径，解压文件夹路径）'''
    # file_extension = os.path.splitext(zip_file_path)
    file_extension = zip_file_path.split('.')
    if (file_extension[-1] == 'gz' and file_extension[-2] == 'tar') or file_extension[-1] == '.tar':
        untar_file(zip_file_path, file_unzip_folder_path)
    elif file_extension[-1] == 'zip':
        unzip_file(zip_file_path, file_unzip_folder_path)
    else:
        print('无法解压该文件！')

def callbackfunc(blocknum, blocksize, totalsize):
    '''下载进度条(已经下载的数据块,数据块的大小,远程文件的大小)'''
    if not totalsize == -1: # 旧的FTP服务器上，它不返回文件大小（下载大遥控器包时），此时参数为-1
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