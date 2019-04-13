#!/usr/bin/env python
#coding=utf-8

import os
import json
import urllib.request
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest


domain = "daha.wiki"
rr = "nas"
client = AcsClient('LTAIN5fW02KpkQNr', 'mFhCLjsVbzpqNQGuAYBN6Qe8JLVhCH', 'cn-hangzhou')


# python2:  print(response)

# 获取域名RecordId
def getRecord():
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')

    request.set_DomainName(domain)

    response = client.do_action_with_exception(request)
    response = json.loads(response.decode("UTF-8"))
    for item in response["DomainRecords"]["Record"]:
        if item['RR'] == rr:
            return item


def getIP():
    html = urllib.request.urlopen('http://jsonip.com').read()
    ip = json.loads(html.decode('utf-8'))['ip']
    return ip


def Dns():
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')

    print('正在获取RecordId……')
    record = getRecord()
    recordId = record['RecordId']

    print("获取成功:%s" % recordId)
    print("获取本机IP……")
    ip = getIP()
    print("获取成功:%s" % ip)

    if ip == record['Value']:
        return print("IP一致无需更新")

    request.set_Value(ip)
    request.set_RecordId(recordId)
    request.set_RR(rr)
    request.set_Type("A")

    print("正在更新DNS……")
    response = client.do_action_with_exception(request)
    return json.loads(response.decode("UTF-8"))

if __name__ == "__main__":
    try:
        result = Dns()
        print(result)
    except (ServerException, ClientException) as reason:
        print("失败！原因为")
        print(reason.get_error_msg())