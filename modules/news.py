import logging
import string
import sys
import feedparser
import threading
import unicodedata

from core.alive import Alive

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

        self.modulename = 'News'
        self.url = None
        self.parsedurl = None
        self.channelname = None
        self.itemsnumber =  None
        threading.Thread.__init__(self)
        self.speak = voicesynthetizer
        self.initialize()

    def alive(self):
        self.alive = Alive()
        self.alive.report(self.modulename)

    def initialize(self):
        self.seturl("http://www.eluniversal.com.mx/rss/universalmxm.xml")
        self.seturl("http://www.eluniversal.com.mx/rss/notashome.xml")
        self.seturl("http://www.eluniversal.com.mx/rss/computo.xml")
        self.parseurl()
        self.setchannel("national")
        self.setitemsnumber("1")
        self.gettitle()

    def seturl(self, url):
        self.url = url

    def geturl(self):
        return self.url

    def parseurl(self):
        self.parsedurl = feedparser.parse(self.url)

    def setchannel(self, channelname):
        self.channelname = channelname

    def getchannel(self):
        return self.channelname

    def setitemsnumber(self, itemsnumber):
        self.itemsnumber = itemsnumber

    def channels(self):
        pass

    def getitemsnumber(self):
        return self.itemsnumber

    def gettitle(self):
        newsdata = self.parsedurl
        channel = newsdata.feed

    def getitems(self):

        logging.info('News Get Items')
        self.alive()
        newsdata = self.parsedurl
        items = newsdata.entries

        for item in items[0:2]:
            messagetitle = item['title'].replace("&quot;", "")
            messagetitle = messagetitle.replace("#39;", "")
            messagedescription = item['description'].replace("&quot;", "")
            messagedescription = messagedescription.replace("#39;", "")
            if not messagetitle.startswith("<img"):
                message = messagetitle
            if not messagedescription.startswith("<img"):
                message = message + ', ' + messagedescription
            self.speak.speechit(message)

# End of File
