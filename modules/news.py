import string
import sys
import feedparser
import threading
import unicodedata

COMMON_CHANNEL_PROPERTIES = [
    ('Channel title:', 'title', None),
    ('Channel description:', 'description', 150),
    ('Channel URL:', 'link', None),
]

COMMON_ITEM_PROPERTIES = [
    ('Item title:', 'title', None),
    ('Item description:', 'description', 150),
    ('Item URL:', 'link', None),
]

INDENT = u' '*4

class News(threading.Thread):
	def __init__(self, voicesynthetizer):
		self.url = None
		self.parsedurl = None
		self.channelname = None
		self.itemsnumber =  None
		threading.Thread.__init__(self)
		self.speak = voicesynthetizer
		self.initialize()

	def initialize(self):
		self.seturl("http://www.eluniversal.com.mx/rss/notashome.xml")
		self.parseurl()
		self.setchannel("national")
		self.setitemsnumber("1")
		self.gettitle()

	def seturl(self, url):
		self.url = url
		print "url? " + self.url

	def geturl(self):
		return self.url

	def parseurl(self):
		self.parsedurl = feedparser.parse(self.url)

	def setchannel(self, channelname):
		self.channelname = channelname
		print "channel name? " + self.channelname

	def getchannel(self):
		return self.channelname

	def setitemsnumber(self, itemsnumber):
		self.itemsnumber = itemsnumber
		print "items number? " + self.itemsnumber

	def channels(self):
		print "channels"

	def getitemsnumber(self):
		return self.itemsnumber

	def gettitle(self):
		newsdata = self.parsedurl
		channel = newsdata.feed

	def remove_accents(self, input_str):
		nkfd_form = unicodedata.normalize('NFKD', input_str)
		only_ascii = nkfd_form.encode('ASCII', 'ignore')
		return only_ascii

	def getitems(self):
                newsdata = self.parsedurl
                items = newsdata.entries

		for item in items[0:5]:
                        messagetitle = self.remove_accents(item['title'])
                        messagedescription = self.remove_accents(item['description'])
			if self.speak.getsynthetizer() == "google":
				messagetitle = "\"" + messagetitle + "\""
				messagedescription = "\"" + messagedescription + "\""
			self.speak.speechit(messagetitle)
			self.speak.speechit(messagedescription)

if __name__ == "__main__":

	mynews = News()

	mynews.seturl("http://www.eluniversal.com.mx/rss/universalmxm.xml")
	mynews.seturl("http://www.eluniversal.com.mx/rss/computo.xml")
	mynews.setchannel("national")
	mynews.setitemsnumber("1")
	mynews.parseurl()

	title = mynews.gettitle()
	mynews.getitems()

