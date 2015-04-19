#!/usr/bin/python

import logging
import ConfigParser

from core.aprsnet import AprsNet
from core.system import System
from core.twitterc import TwitterC
from core.utilities import Randomizer

def alive(module=None, media=None):

    logging.info('Alive')

    aprs = AprsNet()
    conf = ConfigParser.ConfigParser()
    system = System()
    twitterc = TwitterC('twython')

    path = "configuration/general.config"
    conf.read(path)

    twitteraccount = conf.get("general", "twitter")
    hashtag = conf.get("system", "hashtag")
    location =  conf.get("general", "location")
    systemfrequency = conf.get("general", "frequency")
    systemcoordinates = conf.get("general", "coordinates")

    cpu = system.cpu()
    memory = system.memory()
    kernel = system.kernelVersion()

    callsign = conf.get("general", "callsign") + '-1'
    aprs.address_set(callsign)

    cpu = 'Cpu ' + cpu + '%'
    memory = 'Memory ' + memory
    kernel = 'Kernel ' + kernel
    system = ' ' + cpu + ' ' + memory + ' ' + kernel

    message = Randomizer(2) + ' ' + hashtag + ' '
    if module:
        message = message + '#' + module + ' '
    message = message + twitteraccount + ' ' + location
    technical = ' Freq ' + systemfrequency + system
    message = message + ' ' + technical

    aprs.send_message(technical)
    aprs.position_set(systemcoordinates)
    if media:
        twitterc.timeline_set(message, media)
    else:
        twitterc.timeline_set(message, media=None)
    logging.info(message)

# End of File
