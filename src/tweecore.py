import tweepy
import json
import time

__DEBUG__ = True

class DoAuth(object):
	"""docstring for ClassName"""
	def __init__(self):
		self.APIKey = "yZ2IIZLtwRzgrUwuhJxAFGYxh"
		self.APISecret = "e33QxsLEDkXBzVMzJJP6bGgQUGiPR0l2xFbV6LYr5Rm4NU4cq3"
		self.AccessToken = "4905001899-rYjepLfO8IdIMkSBrrwXJs6Wbd4Eo6S9eMjshYR"
		self.AccessTokenSecret = "AMH3YGv5jPc2I5kXw2Dq3Rchios8z78IErvbSMwCIyteA"
	def doauth(self):
		auth = tweepy.OAuthHandler(self.APIKey,self.APISecret)
		auth.set_access_token(self.AccessToken,self.AccessTokenSecret)
		return auth
	def doapi(self,arg):
		return tweepy.API(arg)


def CallRatelimit(func):
	def _deco(s,x):
		s60s = ["process_follow","process_friend"]
		s30s = ["process_status"]
		ret = func(s,x)
		if __DEBUG__:
			time.sleep(3)
		else:
			if func.func_name in s30s:
				time.sleep(30)
			else:
				time.sleep(60)
		return ret
	return _deco


class UserObj():
	def __init__(self,twapi,uid,uname=None):
		self.uid = uid
		self.uname = uname
		self.twapi = twapi
		self.followersidlst = []
		self.friendsid = []
		self.relKey = "id"
		self.FOLLOW = 1
		self.FRIEND = 2
	def get_user_info(self):
		if self.uname == None:
			self.userobj = self.twapi.get_user(self.uid)
		else:
			self.userobj = self.twapi.get_user(self.uname)
		return self._processret(self.userobj)

	def get_followers_page(self):
		for page in tweepy.Cursor(self.twapi.followers,id=self.uid).pages():
		# return self.api.followers()
			yield self.process_follow(page)

	def get_friends_page(self):
		for page in tweepy.Cursor(self.twapi.friends,id=self.uid).pages():
			yield self.process_friend(page)

	@CallRatelimit
	def process_follow(self,pagedata):
		return	self.processret(pagedata,self.FOLLOW)

	@CallRatelimit
	def process_friend(self,pagedata):
		return  self.processret(pagedata,self.FRIEND)
	
	def processret(self,items,source):
		resultlst = [self._processret(x) for x in items]
		self._append_lst(source,resultlst)
		return resultlst

	def _processret(self,item):
		ret = {}
		# for key in item.__dict__:
			# print type(item.__dict__[key])
			# print key," : ",item.__dict__[key],"\n\n\n\n"
			# ret[key] = item.__dict__[key]
			# self.followersidlst.append(item.__dict__["id"])	
		# return ret
		return item._json
		# return json.loads(json.dumps(item._json))

	def _append_lst(self,source,slst):
		if source == self.FOLLOW: #follow
			self.followersidlst += self._mk_lst(slst)
		elif source == self.FRIEND: #friend
			self.friendsid += self._mk_lst(slst)

	def _mk_lst(self,slst):
		return [item[self.relKey] for item in slst]

	def show_relids(self,tag):
		if tag == 1:
			return self.followersidlst
		elif tag == 2:
			return self.friendsid
		elif tag == 0:
			return {"id":self.uid,"follows":self.followersidlst,"friends":self.friendsid}


class SearchUser():
	def __init__(self):
		pass
	def search_by_name(self):
		pass

class Status():
	def __init__(self,twapi,uid):
		self.twapi = twapi
		self.uid = uid

	def usr_timeline(self):
		self.twobj = self.twapi.user_timeline(self.uid)
		return self.twobj
	def get_status_page(self):
		for page in tweepy.Cursor(self.twapi.user_timeline,id=self.uid).pages():
			yield self.process_status(page)

	@CallRatelimit
	def process_status(self,pagedata):
		resultlst = [self._processret(item) for item in pagedata]
		return resultlst

	# def processret(self,pagedata):
	# 	pass

	def _processret(self,item):
		ret = {}
		# for key in item.__dict__:
		# 	ret[key] = item.__dict__[key]
		# return ret
		return item._json

######    test...
if __name__ == '__main__':

	# test
	doauth = DoAuth()
	auth = doauth.doauth()
	api = doauth.doapi(auth)

	def testUserObj():
		user = UserObj(api,2875746901)
		for page in user.get_followers_page():
			print "One page followers len:",len(page),"\n\n\n\n\n"


		for page in user.get_friends_page():
			print "One page friends len:",len(page),"\n\n\n\n\n"

		print user.show_relids(0)
		print "follows len:",len(user.show_relids(1)),"  friends len:",len(user.show_relids(2))
	def testStatus():
		status = Status(api,2875746901)
		create_dtlst = []
		for page in status.get_status_page():
			print "On Page status len :",len(page)
			for item in page:
				create_dtlst.append(item["created_at"])
		print create_dtlst
	# testStatus()

	### old way
	# page = 1
	# while True:
	# 	statuses = api.user_timeline(page=page)
	# 	if statuses:
	# 		for status in statuses:
	# 			print status
	# 	else:
	# 		break
	# 	page += 1 


	# ret = api.followers(id=203829129)
	# ret = ret[0]
	# print ret,"\n\n\n\n\n\n\n\n"

	# print dir(ret)
	# print type(ret),"\n\n\n\n\n\n\n\n"

	# for key in ret.__dict__:
	# 	print key

	
	###### new cursor way
	# for status in tweepy.Cursor(api.user_timeline).items(): #pages() #items(300)  #pages(3)
	# 	print status

	# for item in tweepy.Cursor(api.followers,id=203829129).pages():
	# 	print item
	# 	time.sleep(10)

	# loop = 0
	# for page in tweepy.Cursor(api.followers,id=203829129,page=18).pages():
	# 	time.sleep(10)
	# 	loop += 1
	# 	print page
	# 	print "loop:",loop

	# public_tweets = api.home_timeline()
	# for item in public_tweets:
	# 	print item
	uobj = UserObj(api,uid = 203829129)
	uobj.get_user_info()

# api.xxx()