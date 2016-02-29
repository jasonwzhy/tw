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
        time.sleep(5)
        for item in itemiterator['Items']:
            ucount += 1
            dict = {'id':item['id']['N'],'text':item['text']['S'],'userid':item['userid']['N']}
            fp.writelines(json.dumps(dict,ensure_ascii=False))
    print ucount
def exportstatus(tb):
    response = tb.scan(

        FilterExpression=Attr('id').gt(0)
    )
    for item in response['Items']:
        print item
    # items = response['Items']

# tb = InitDyDB('Tweestatus')
# exportstatus(tb)
DyDBClient()