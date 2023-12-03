import logging
import feedparser
import random
import threading

from core.alive import alive
from bs4 import BeautifulSoup

INDENT = u' ' * 4

class News(threading.Thread):
    """
    The News class fetches news items from RSS feeds and reads them using a voice synthesizer.
    """

    def __init__(self, voicesynthetizer):
        self.modulename = 'News'
        self.url = None
        self.parsedurl = None
        self.channelname = None
        self.itemsnumber = None
        threading.Thread.__init__(self)
        self.speak = voicesynthetizer
        self.initialize()

    def initialize(self):
        rss_urls = [
            #"http://www.reforma.com/rss/portada.xml",
            #"https://wwww.vanguardia.com.mx/rss.xml",
            "https://www.elsiglodetorreon.com.mx/index.xml"
            # Add more RSS URLs here
        ]
        self.set_url(random.choice(rss_urls))
        print(self.url)
        self.parse_url()
        self.parse_url()
        self.set_channel("national")
        self.set_items_number("1")
        self.get_title()

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def parse_url(self):
        self.parsedurl = feedparser.parse(self.url)

    def set_channel(self, channelname):
        self.channelname = channelname

    def get_channel(self):
        return self.channelname

    def set_items_number(self, itemsnumber):
        self.itemsnumber = itemsnumber

    def get_items_number(self):
        return self.itemsnumber

    def get_title(self):
        newsdata = self.parsedurl
        channel = newsdata.feed

    def get_items(self):
        """
        Fetch news items and read them using a voice synthesizer.
        """
        logging.info('News Get Items')
        newsdata = self.parsedurl
        #print(newsdata)
        items = newsdata.entries
        #print(items)

        for item in items[0:2]:
            messagetitle = item['title'].replace("&quot;", "")
            messagetitle = messagetitle.replace("#39;", "")
            messagedescription = item['description'].replace("&quot;", "")
            messagedescription = messagedescription.replace("#39;", "")
            if not messagetitle.startswith("<img"):
                message = messagetitle
            if not messagedescription.startswith("<img"):
                message = message + ', ' + messagedescription
            message = BeautifulSoup(message, 'html.parser')
            message = message.get_text()
            print(message)
            self.speak.speech_it(message)
            # alive(modulename=self.modulename, modulemessage=message)

# End of File
