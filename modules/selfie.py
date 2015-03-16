#!/usr/bin/python

import ConfigParser
import logging
import random

from core.camera import Camera
from core.phonetic import Phonetic
from core.twitterc import TwitterC
from core.utilities import Randomizer

class Selfie(object):

    def __init__(self, voicesynthetizer):

	self.camera = Camera(voicesynthetizer)
        self.phonetic = Phonetic()
	self.twitterc = TwitterC('twython')
        self.voicesynthetizer = voicesynthetizer

    def setup(self):

        logging.info('Selfie Setup')
        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

    def get(self):

        logging.info('Selfie Get')
        self.setup()

        try:
            self.camera.execute()
            message = Randomizer(2) + ' ' + self.conf.get("system", "hashtag") + ' #Selfie '
            message = message + 'Voice Experimental Station ... Visit me @ https://github.com/xe1gyq/cancun'
            logging.info(message)
            media='output/camerapygame.jpg'
            self.twitterc.timeline_set(message, media)
            message = "Hola! Mi selfie en twitter.com/ " + ' arjac cancun'
            self.voicesynthetizer.speechit(message)
            message = ' '.join(self.phonetic.decode("arjaccancun"))
            self.voicesynthetizer.speechit(message)
        except:
            logging.error('Cannot open Camera device')


# End of File
