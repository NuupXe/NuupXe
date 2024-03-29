#!/usr/bin/python

import logging
import configparser
#from backports import configparser

from core.aprsnet import AprsNet
from core.system import System
from core.twitterc import TwitterC
from core.utilities import Randomizer

def alive(modulename=None, modulemessage=None, media=None):

    logging.info('Alive')

    #aprs = AprsNet()
    conf = configparser.ConfigParser()
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
    #aprs.address_set(callsign)

    cpu = 'Cpu ' + str(cpu) + '%'
    memory = 'Memory ' + str(memory)
    kernel = 'Kernel ' + str(kernel)
    system = ' ' + cpu + ' ' + memory + ' ' + kernel

    message = Randomizer(2) + ' ' + hashtag + ' '
    if modulename:
        message = message + '#' + modulename + ' '
    message = message + twitteraccount + ' ' + location
    technical = ' Freq ' + systemfrequency + system
    if modulemessage:
        message = message + ' ' + modulemessage
    else:
        message = message + ' ' + technical

    #aprs.send_message(technical)
    #aprs.position_set(systemcoordinates)
    message = (message[:136] + '...')
    return
    if media:
        message = (message[:110] + '...')
        twitterc.timeline_set(message, media=media)
    else:
        twitterc.timeline_set(message, media=None)
    logging.info(message)

# End of File
