# HCTools使用说明
* 可用于获取飞机信息、设置飞机相关配置
* 运行环境 python 3

## Useage
#### 获取帮助
```
python3 HCTool.py -h
```
#### 获取飞机信息
```
python3 HCTool.py -g
```
#### 更改Wi-Fi密码
```
python3 HCTool.py -p NewPass
```
#### 更改Wi-Fi频段
```
python3 HCTool.py -w 5   //改为5G
python3 HCTool.py -w 2   //改为2.4G
```
#### 更改SSID
```
python3 HCTool.py -s NewSSID
```
#### 升级IPK
```
python3 HCTool.py -i dev    // 升级为dev最新版本
python3 HCTool.py -i totest // 升级为totest最新版本
```
#### 升级天空端
```
python3 HCTool.py -k dev    // 升级为dev最新版本
python3 HCTool.py -k totest // 升级为totest最新版本
python3 HCTool.py -k local_file.bin // 使用本地文件进行升级
```
### Feedback
E-mail：jishuhan@zerozero.cn