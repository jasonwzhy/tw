#!usr/bin/python
# coding=utf-8
from TerrorTrendency.model_base_dict import *
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import sys
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
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tb)

    table.update_item(
        Key=keymap,
        UpdateExpression='SET scorev1 = :val1',
        ExpressionAttributeValues={
            ':val1': scorenum
        }
    )
    # response = table.get_item(
    # Key={
    #         'Artist': 'ah00ha',
    #         'SongTitle':'minigh'
    #     }
    # )
    # item = response['Item']
    # print item


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
            'userid'
        ]
    )
    for itemiterator in response_iterator:
        # time.sleep(1)
        for item in itemiterator['Items']:
            dict = {'id':item['id']['N'],'text':item['text']['S'],'userid':item['userid']['N']}
            # print json.dumps(dict,ensure_ascii=False)
            UpdateItem(
                tbname,
                {'id':item['id']['N'],'created_at_ts':item['created_at_ts']['N']},
                terror.getPaperTrendency(json.dumps(dict,ensure_ascii=False))*10
            )
            # print terror.getPaperTrendency(json.dumps(dict,ensure_ascii=False))
        # print 'current loop:',ucount
def TagScoreToUsers():
    usertb = 'TweeUsers'
    statustb = 'Tweestatus'
    terror = TerrorModel()
    client = boto3.client('dynamodb')
    #scan user return userid
    paginator = client.get_paginator('scan')
    paginatorqstat = client.get_paginator('query')
    response_iterator = paginator.paginate(
        Select='SPECIFIC_ATTRIBUTES',
        TableName=usertb,
        ProjectionExpression = 'id',
    )
    for itemiterator in response_iterator:
        for item in itemiterator['Items']:
            cur_userid = item['id']['N']
            userstatusscorelst = []
            # query user`s status by userid
            qstatresponse_iterator = paginatorqstat.paginate(
                Select='SPECIFIC_ATTRIBUTES',
                TableName=statustb,
                ProjectionExpression = 'id',
                FilterExpression='userid=:uid',
                ExpressionAttributeValues={
                    ':uid':{
                        'N':cur_userid
                    }
                }
            )
            for qstatuslst in qstatresponse_iterator:
                for userstatus in qstatuslst['Items']:
                    if 'scorev1' in userstatus:
                        userstatusscorelst.append(userstatus['scorev1']['N'])
            userscore = terror.getPersonTerrorTendency(userstatusscorelst)
            UpdateItem(usertb,{'id':cur_userid},userscore)


if __name__ == "__main__":
    TagScoreToTwstatus()
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