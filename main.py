#!/usr/bin/env python
#coding=utf-8

import os
import json
import urllib.request
import logging
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest


domain = "daha.wiki"
rr = "nas"
client = AcsClient('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')


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

    logging.info("Getting RecordId....")
    record = getRecord()
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
    request.set_RR(rr)
    request.set_Type("A")

    response = client.do_action_with_exception(request)
    return json.loads(response.decode("UTF-8"))

if __name__ == "__main__":
    try:
        logging.basicConfig(filename='log_examp.log', level=logging.INFO)
        result = Dns()
        logging.info(result)
    except (ServerException, ClientException) as reason:
        logging.info(reason.get_error_msg())