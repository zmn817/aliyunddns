#阿里云动态解析（DDNS）

###配置阿里云

1. 添加RAM子账号（https://ram.console.aliyun.com/users）
2. 设置权限：AliyunHTTPDNSFullAccess(管理HTTPDNS的权限)与AliyunHTTPDNSFullAccess(管理云解析(DNS)的权限)
3.手动创建一个子域名

###群晖安装pip3
```
sudo -i
wget -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py'
python3 /tmp/get-pip.py ""pip==8.1.2""
rm /tmp/get-pip.py
```

###安装项目依赖
```
python3 -m virtualenv --no-site-packages venv
venv/bin/pip3 install -r requirements.txt
```

###配置文件
新建config.json配置文件，按以下格式填写内容
```json
{
  "domain": "", // 域名
  "rr": ["www","demo"], // 主机记录
  "accessKeyId": "", // 阿里访问KEYID
  "accessSecret": "", // 阿里访问 Secret
  "regionId": "cn-hangzhou" // 解析地址
}
```

###配置定时任务
```sh
#! /bin/bash
cd <你的项目路径>/aliyunddns/
venv/bin/python main.py
```