#!usr/bin/python
# coding=utf-8
from TerrorTrendency.model_base_dict import *
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')
import decimal
__test__ = False

def IteratorUser():
    # user_iterator = paginator.paginate(
    #     Select = 'SPECIFIC_ATTRIBUTES',
    #     TableName = 'TweeUsers',
    #
    # )
    pass



def UpdateItem(tb,keymap,scorenum):
    # tb = 'Tweestatus'
    print tb,' ',keymap,'  ',scorenum
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tb)
    time.sleep(0.2)
    table.update_item(
        Key=keymap,
        UpdateExpression='SET scorev1 = :val1',
        ExpressionAttributeValues={
            ':val1': scorenum
        }
    )


def TagScoreToTwstatus():
    tbname = 'Tweestatus'
    terror = TerrorModel()

    client = boto3.client('dynamodb')
    paginator = client.get_paginator('scan')

    response_iterator = paginator.paginate(
        Select='SPECIFIC_ATTRIBUTES',
        TableName=tbname,
        AttributesToGet=[
            'id',
            'text',
            'userid',
            'created_at_ts'
        ]
    )
    for itemiterator in response_iterator:
        # time.sleep(1)
        for item in itemiterator['Items']:
            dict = {'id':item['id']['N'],'text':item['text']['S'],'userid':item['userid']['N']}
            # print json.dumps(dict,ensure_ascii=False)
            UpdateItem(
                tbname,
                {'id':int(item['id']['N']),'created_at_ts':int(item['created_at_ts']['N'])},
                int(terror.getPaperTrendency(json.dumps(dict,ensure_ascii=False))*10)
            )
            # print terror.getPaperTrendency(json.dumps(dict,ensure_ascii=False))
        # print 'current loop:',ucount

def TagScoreToUsers():
    usertb = 'TweeUsers'
    statustb = 'Tweestatus'
    statustbindex = 'userid-index'
    terror = TerrorModel()
    client = boto3.client('dynamodb')
    #scan user return userid
    paginator = client.get_paginator('scan')
    paginatorqstat = client.get_paginator('scan')
    response_iterator = paginator.paginate(
        Select='SPECIFIC_ATTRIBUTES',
        TableName=usertb,
        ProjectionExpression = 'id,statuses_count',
    )
    for itemiterator in response_iterator:
        for item in itemiterator['Items']:
            cur_userid = item['id']['N']
            cur_statcount = item['statuses_count']['N']
            print '[current userid] ',cur_userid
            print '[current statcount]',cur_statcount
            if cur_statcount != '0':
                userstatusscorelst = []
                # query user`s status by userid
                qstatresponse = client.scan(
                    Select='SPECIFIC_ATTRIBUTES',
                    TableName=statustb,
                    IndexName=statustbindex,
                    Limit=200,
                    ProjectionExpression = 'id,scorev1',
                    FilterExpression='userid=:uid',
                    ExpressionAttributeValues={
                        ':uid':{
                            'N':cur_userid
                        }
                    }

                )
                # qstatresponse_iterator = paginatorqstat.paginate(
                #     Select='SPECIFIC_ATTRIBUTES',
                #     TableName=statustb,
                #     IndexName=statustbindex
                #     ProjectionExpression = 'id,scorev1',
                #     FilterExpression='userid=:uid',
                #     ExpressionAttributeValues={
                #         ':uid':{
                #             'N':cur_userid
                #         }
                #     }
                # )
                # for qstatuslst in qstatresponse_iterator:
                #     for userstatus in qstatuslst['Items']:
                #         print userstatus['id']
                #         if 'scorev1' in userstatus:
                #             userstatusscorelst.append(userstatus['scorev1']['N']/10.0)
                for curstatus in qstatresponse['Items']:
                    if 'scorev1' in curstatus:
                        userstatusscorelst.append(float(curstatus['scorev1']['N'])/10.0)
                print '[userstatusscorelst len]', len(userstatusscorelst)
                print '---------------------------------'
                userscore = terror.getPersonTerrorTendency(userstatusscorelst)
                UpdateItem(usertb,{'id':int(cur_userid)},int(userscore*10))


if __name__ == "__main__":
    # TagScoreToTwstatus()
    TagScoreToUsers()

# if __test__:
    # TagScoreToTwstatus()
    # UpdateItem('Music',{'id':1},3)
    # client = boto3.client('dynamodb')
    # paginatorqstat = client.get_paginator('scan')
    # qstatresponse_iterator = paginatorqstat.paginate(
    #     Select='SPECIFIC_ATTRIBUTES',
    #     TableName='Tweestatus',
    #     # AttributesToGet=[
    #     #     'id'
    #     # ],
    #     ProjectionExpression = 'id,userid',
    #     # KeyConditionExpression='id=:id AND created_at_ts=:ts',
    #     # ScanFilter={
    #     #     'userid':{
    #     #         'AttributeValueList':[
    #     #             {
    #     #                 'N':'3033102862'
    #     #             }
    #     #         ],
    #     #         'ComparisonOperator':'EQ'
    #     #     }
    #     # },
    #     FilterExpression='userid=:uid',
    #     ExpressionAttributeValues={
    #         ':uid':{
    #             'N':'3033102862'
    #         }
    #     },
    #     # ExpressionAttributeNames={
    #     #     '#uid':'userid'
    #     # }
    #
    #     # KeyConditionExpression='userid = :partitionkeyval',
    #     # FilterExpression='userid = 3033102862',
    #     # ExpressionAttributeNames={
    #     #     'partitionkeyval':3033102862
    #     # }
    # )
    # for items in qstatresponse_iterator:
    #     for i in items['Items']:
    #         print i