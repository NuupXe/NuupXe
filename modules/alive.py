#!/usr/bin/python

import logging
import ConfigParser

from core.aprsnet import AprsNet
from core.randomizer import randomize
from core.system import System
from core.twitterc import TwitterC

class Alive(object):

    def __init__(self):

        self.aprs = AprsNet()
        self.system = System()
        self.twitterc = TwitterC('twython')

    def setup(self):

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

        callsign = self.conf.get("general", "callsign") + '-1'
        self.aprs.address_set(callsign)
        self.aprs.position_set(self.conf.get("general", "coordinates"))

    def report(self):

        self.setup()

        system = self.system.execute()
        message = randomize(2) + ' ' + self.conf.get("system", "hashtag") + ' '
        message = message + self.conf.get("general", "twitter") + ' Frequency ' + self.conf.get("general", "frequency")
        message = message + ' .. ' + system

        logging.info(message)
        self.aprs.send_message(system)
        self.twitterc.timeline_set(message, media=None)
        self.twitterc.timeline_get('arjaccancun', 1)

# End of File
