#!/usr/bin/python

import logging
import ConfigParser

from core.randomizer import randomize
from core.twitterc import TwitterC

class Alive(object):

    def __init__(self):

	self.twitterc = TwitterC('twython')
        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

    def report(self):
        message = randomize(6) + ' ' + self.conf.get("system", "hashtag") + ' '
        message = message + self.conf.get("general", "twitter") + ' '
        message = message + self.conf.get("general", "radioclub") + ' @ ' + self.conf.get("general", "frequency")
        logging.info(message)
        self.twitterc.timeline_set(message, media=None)
        self.twitterc.timeline_get('arjaccancun', 1)

# End of File
