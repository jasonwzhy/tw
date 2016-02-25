#!usr/bin/python
#coding=utf-8

import tweecore
from tweecore import DoAuth, UserObj, SearchUser, Status
import boto3
import json
import decimal
import time
from datetime import datetime

# Must config the Access Keys & Region first
# Configure the Access Keys

SeedLst = [203829129,45358339]
class InitDynamoDB():
	def __init__(self,tables):
		dynamodb = boto3.resource('dynamodb')
		self.tb = dynamodb.Table(tables)
	def putdata(self,data):
		# if type(data) == str:
		# 	itemdata = self._serialization(json.loads(data))
		# elif type(data) == dict:
		# 	itemdata = self._serialization(data)
		# else:
		# 	return -1
		self.tb.put_item(Item=self._serialization(data))

	def _serialization(self,mapdata):
		tmpmap = {}
		jdump = json.dumps(mapdata)
		if "" in jdump:
			jdump = jdump.replace('""',"null")
		elif '' in jdump:
			jdump = jdump.replace("''","null")
		mapdata = json.loads(jdump, parse_float=decimal.Decimal)
		for k,v in mapdata.items():
			if v == "":
				tmpmap[k] = None
			elif isinstance(v, float):
				tmpmap[k] = str(v)
			else:
				tmpmap[k] = v
		print tmpmap,"\n\n\n"
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

		uinfo["seed"] = True
		tbusr.putdata(uinfo)
	
		procstatus(tbstat,api,seedusr)
		


		for pagedata in user.get_followers_page():
			for item in pagedata:
				try:
					item["seed"] = False
					tbusr.putdata(item)
					procstatus(tbstat,api,item["id"])
				except Exception, e:
					print Exception,e
					continue
		
		for pagedata in user.get_friends_page():
			for item in pagedata:
				try:
					item["seed"] = False
					tbusr.putdata(item)
					procstatus(tbstat,api,item["id"])
				except Exception, e:
					print Exception,e
					continue

		tbrel.putdata(user.show_relids())


def procstatus(table,api,uid):
	status = Status(api,uid)
	for statuspage in status.get_status_page():
			for item in statuspage:
				# print item
				item["userid"] = uid
				#Wed Feb 24 13:15:59 +0000 2016
				try:
					if "created_at" in item:
						if item["created_at"] != None or item["created_at"] != "":
							timestr = item["created_at"]
							dt = datetime.strptime(timestr, '%a %b %d %X  %Y')
							ts = int(time.mktime(dt.timetuple()))
							item["created_at_ts"] = ts
					table.putdata(item)
				except Exception, e:
					print Exception,e
					continue
				



if __name__ == '__main__':
	dosync_twee()


	# tbusr.putdata(mydic)
	# tb = InitDynamoDB("Music")
	# myd = {"fdsa":"fdsa","id":312,"Artist":"fdsfads","SongTitle":"fdsafds"}
	# tb.putdata(myd)