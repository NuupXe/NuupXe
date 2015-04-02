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

        self.setup()

    def setup(self):

        logging.info('Alive Setup')

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

        self.twitteraccount = self.conf.get("general", "twitter")
        self.hashtag = self.conf.get("system", "hashtag")
        self.systemfrequency =  self.conf.get("general", "frequency")
        self.systemcoordinates = self.conf.get("general", "coordinates")

        self.cpu = self.system.cpu()
        self.memory = self.system.memory()
        self.kernel = self.system.kernelVersion()

        callsign = self.conf.get("general", "callsign") + '-1'
        self.aprs.address_set(callsign)

    def report(self):

        logging.info('Alive Report')

        cpu = 'Cpu ' + self.cpu + '%'
        memory = 'Memory ' + self.memory
        kernel = 'Kernel ' + self.kernel
        system = ' ' + cpu + ' ' + memory + ' ' + kernel

        message = Randomizer(2) + ' ' + self.hashtag + ' '
        message = message + self.twitteraccount 
        technical = ' Freq ' + self.systemfrequency + system
        message = message + ' ' + technical

        self.aprs.send_message(technical)
        self.aprs.position_set(self.systemcoordinates)
        self.twitterc.timeline_set(message, media=None)
        logging.info(message)

# End of File
