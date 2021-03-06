#!usr/bin/python
# coding=utf-8
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')


def InitDyDB(Tname):
    dydb = boto3.resource('dynamodb')
    dytb = dydb.Table(Tname)
    return dytb

def DyDBClient():
    client = boto3.client('dynamodb')
    paginator = client.get_paginator('scan')
    response_iterator = paginator.paginate(
        Select = 'SPECIFIC_ATTRIBUTES',
        TableName='Tweestatus',
        AttributesToGet=[
            'id',
            'text',
            'userid'

            # 'coordinates'
        ]
        # ProjectionExpression='text,coordinates'
    )
    ucount = 0
    fp = open('./outputstatus','w+r')
    for itemiterator in response_iterator:
        time.sleep(60)
        for item in itemiterator['Items']:
            ucount += 1
            dict = {'id':item['id']['N'],'text':item['text']['S'],'userid':item['userid']['N']}
            fp.writelines(json.dumps(dict,ensure_ascii=False)+"\n")
        print 'current loop:',ucount
def DyDBClientUser():
    client = boto3.client('dynamodb')
    paginator = client.get_paginator('scan')
    response_iterator = paginator.paginate(
        Select = 'SPECIFIC_ATTRIBUTES',
        TableName='Tweestatus',
        AttributesToGet=[
            'id'
        ]
    )
    fp = open('./outputuserid','w+r')
    for itemiterator in response_iterator:
        # time.sleep(1)
        for item in itemiterator['Items']:
            # ucount += 1
            # print "%d,"%int(item['id']['N'])
            # dict = {'id':item['id']['N'],'text':item['text']['S'],'userid':item['userid']['N']}
            fp.write(item['id']['N']+u",")
        # print 'current loop:',ucount

def exportstatus(tb):
    response = tb.scan(

        FilterExpression=Attr('id').gt(0)
    )
    for item in response['Items']:
        print item
    # items = response['Items']


# tb = InitDyDB('Tweestatus')
# exportstatus(tb)
# DyDBClient()
DyDBClientUser()