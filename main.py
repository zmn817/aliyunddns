#!/usr/bin/env python
#coding=utf-8

import os
import json
import time
import urllib.request
import logging
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest


domain = "" # map.baidu.com domain = baidu.com
rr = [] # map.baidu.com RR = map
client = ""
configFile = "config.json" # 配置文件位置


# 获取域名RecordId
def getRecord(_rr):
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')

    request.set_DomainName(domain)

    response = client.do_action_with_exception(request)
    response = json.loads(response.decode("UTF-8"))
    for item in response["DomainRecords"]["Record"]:
        if item['RR'] == _rr:
            return item


def getIP():
    html = urllib.request.urlopen('http://jsonip.com').read()
    ip = json.loads(html.decode('utf-8'))['ip']
    return ip


def Dns(_rr):
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')

    logging.info('Update %s.%s DNS' % (_rr, domain))
    logging.info("Getting RecordId....")
    record = getRecord(_rr)
    recordId = record['RecordId']
    logging.info("RecordId:%s" % recordId)

    logging.info("Getting IP....")
    ip = getIP()
    logging.info("IP:%s" % ip)

    if ip == record['Value']:
        return "IP consistency does not need to be updated."

    logging.info("Updating DNS....")
    request.set_Value(ip)
    request.set_RecordId(recordId)
    request.set_RR(_rr)
    request.set_Type("A")

    response = client.do_action_with_exception(request)
    return json.loads(response.decode("UTF-8"))


def init():
    if not os.path.exists(configFile):
        os.system('cp .config.json config.json')

    file = open(configFile, 'r')
    fileJson = file.read()
    file.close()
    config = json.loads(fileJson)

    global domain
    global rr
    global client

    domain = config['domain']
    rr = config['rr']
    client = AcsClient(config['accessKeyId'], config['accessSecret'], config['regionId'])


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='log_examp.log', level=logging.INFO)
        init()

        for _rr in rr:
            result = Dns(_rr)
            logging.info(result)
            strTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logging.info('%s Update %s.%s DNS' % (strTime, _rr, domain))

        logging.info('update completed.')
    except (ServerException, ClientException) as reason:
        logging.info(reason.get_error_msg())