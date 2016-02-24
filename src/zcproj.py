import tweecore
from tweecore import DoAuth, UserObj, SearchUser, Status
import boto3
import json


# Must config the Access Keys & Region first
# Configure the Access Keys

SeedLst = [203829129,45358339]
class InitDynamoDB():
	def __init__(self,tables):
		dynamodb = boto3.resource('dynamodb')
		self.tb = dynamodb.Table(tables)
	def putdata(self,data):
		if type(data) == str:
			itemdata = self._serialization(json.loads(data))
		elif type(data) == dict:
			itemdata = self._serialization(data)
		else:
			return -1
		self.tb.put_item(Item=itemdata)
	def _serialization(self,mapdata):
		tmpmap = {}
		lo = 0
		for k,v in mapdata.items():
			lo += 1
			tmpmap[k] = "fdsafdafa"
			if lo > 7:
				break
		tmpmap["id"]=1231231
		return tmpmap


# class GetuserwithSid():
# 	def __init__(self):
# 		pass

def dosync_twee():
	tbusr = InitDynamoDB("TweeUsers")
	tbstat = InitDynamoDB("Tweestatus")
	tbrel = InitDynamoDB("TweeRel")
	
	doauth = DoAuth()
	auth = doauth.doauth()
	api  = doauth.doapi(auth)

	for seedusr in SeedLst:
		user = UserObj(api,seedusr)

		uinfo = user.get_user_info()
		# uinfo["seed"] = True
		# del(uinfo["status"])
		# for k,v in uinfo.items():
		# 	print k , " : ", v
		# uinfo["id"]=123123123
		tbusr.putdata(uinfo)
		procstatus(tbstat,api,seedusr)


		for pagedata in user.get_followers_page():
			for item in pagedata:
				item["seed"] = False
				tbusr.putdata(item)
				procstatus(tbstat,api,item["id"])
		
		for pagedata in user.get_friends_page():
			for item in pagedata:
				item["seed"] = False
				tbusr.putdata(item)
				procstatus(tbstat,api,item["id"])

		tbrel.putdata(user.show_relids())


def procstatus(table,api,uid):
	status = Status(api,uid)
	for statuspage in status.get_status_page():
		for item in statuspage:
			# print item
			item["userid"] = uid
			item["created_at_ts"] = 0
			table.putdata(item)



if __name__ == '__main__':
	# dosync_twee()
	dynamodb = boto3.resource('dynamodb')
	tb = dynamodb.Table("TweeUsers")
	doauth = DoAuth()
	auth = doauth.doauth()
	api  = doauth.doapi(auth)
	user = UserObj(api,203829129)

	uinfo = user.get_user_info()
	tb.put_item(Item=uinfo)

	# tbusr.putdata(mydic)
	# tb = InitDynamoDB("Music")
	# myd = {"fdsa":"fdsa","id":312,"Artist":"fdsfads","SongTitle":"fdsafds"}
	# tb.putdata(myd)