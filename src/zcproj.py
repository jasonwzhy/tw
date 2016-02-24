import tweecore
from tweecore import DoAuth UserObj SearchUser Status
import boto3
import json


# Must config the Access Keys & Region first
# Configure the Access Keys

SeedLst = [203829129,45358339]
class InitDynamoDB():
	def __init__(self,tables):
		dynamodb = boto3.resource('dynamodb')
		self.tb = dynamodb.Table(tables)
	def put(self,data):
		if type(data) == str:
			itemdata = json.loads(data)
		elif type(data) == dict:
			itemdata = data
		else:
			return -1
		self.tb.put_item(Item=itemdata)

# class GetuserwithSid():
# 	def __init__(self):
# 		pass

def dosync_twee():
	tbusr = InitDynamoDB("TweeUsers")
	tbstat = InitDynamoDB("Tweestatus")
	tbrel = InitDynamoDB("TweeRel")
	
	auth = DoAuth()
	auth = doauth.doauth()
	api  = doauth.doapi(auth)

	for seedusr in SeedLst:
		user = UserObj(api,seedusr)

		uinfo = user.get_user_info()
		uinfo["seed"] = True
		tbusr.put(uinfo)
		procstatus(tbstat,api,seedusr)


		for pagedata in user.get_followers_page():
			for item in pagedata:
				item["seed"] = False
				tbusr.put(item)
				procstatus(tbstat,api,item["id"])
		
		for pagedata in user.get_friends_page():
			for item in pagedata:
				item["seed"] = False
				tbusr.put(item)
				procstatus(tbstat,api,item["id"])

		tbrel.put(user.show_relids())


def procstatus(table,api,uid):
	status = Status(api,seedusr)
	for statuspage in status.get_status_page():
		for item in statuspage:
			table.put(item)



if __name__ == '__main__':
	dosync_twee()