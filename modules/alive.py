#!/usr/bin/python

import logging
import ConfigParser

from core.aprsnet import AprsNet
from core.system import System
from core.twitterc import TwitterC
from core.utilities import Randomizer

class Alive(object):

    def __init__(self):

        self.aprs = AprsNet()
        self.system = System()
        self.twitterc = TwitterC('twython')

    def setup(self):

        logging.info('Alive Setup')
        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

        callsign = self.conf.get("general", "callsign") + '-1'
        self.aprs.address_set(callsign)
        self.aprs.position_set(self.conf.get("general", "coordinates"))

    def report(self):

        logging.info('Alive Report')
        self.setup()

        cpu = self.system.cpu()
        cpu = 'Cpu ' + cpu + '%'
        memory = self.system.memory()
        memory = 'Memory ' + memory
        kernel = self.system.kernelVersion()
        kernel = 'Kernel ' + kernel
        system = ' ' + cpu + ' ' + memory + ' ' + kernel

        message = Randomizer(2) + ' ' + self.conf.get("system", "hashtag") + ' '
        message = message + self.conf.get("general", "twitter") 
        technical = ' Freq ' + self.conf.get("general", "frequency") + system
        message = message + ' ' + technical

        self.aprs.send_message(technical)
        self.twitterc.timeline_set(message, media=None)
        logging.info(message)

# End of File
