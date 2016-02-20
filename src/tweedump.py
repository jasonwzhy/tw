import tweepy
import json
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

class UserObj():
	def __init__(self,twapi,uid,uname=None):
		self.uid = uid
		self.uname = uname
		self.twapi = twapi
		if uname == None:
			self.userobj = self.twapi.get_user(self.uid)
		else:
			self.userobj = self.twapi.get_user(self.uname)
	def get_user_info(self):
		print self.userobj

	def get_followers(self):
		pass

class SearchUser():
	def __init__(self):
		pass
	def search_by_name(self):
		pass

class CursorObj():
	def __init__(self):
		pass

######    test...
if __name__ == '__main__':

	# test
	doauth = DoAuth()
	auth = doauth.doauth()
	api = doauth.doapi(auth)

	### old way
	page = 1
	while True:
		statuses = api.user_timeline(page=page)
		if statuses:
			for status in statuses:
				print status
		else:
			break
		page += 1 
	
	###### new cursor way
	# for status in tweepy.Cursor(api.user_timeline).items(): #pages() #items(300)  #pages(3)
	# 	print status

	# for item in tweepy.Cursor(api.followers,id=203829129).items():
	# 	print item

		
	# public_tweets = api.home_timeline()
	# for item in public_tweets:
	# 	print item
	# uobj = UserObj(api,uid = 203829129)
	# uobj.get_user_info()

# api.xxx()