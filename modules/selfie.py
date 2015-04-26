#!/usr/bin/python

import ConfigParser
import logging
import random

from core.alive import alive
from core.camera import Camera
from core.phonetic import Phonetic
from core.twitterc import TwitterC
from core.utilities import Randomizer

class Selfie(object):

    def __init__(self, voicesynthetizer):

        self.modulename = 'Selfie'
	self.camera = Camera(voicesynthetizer)
        self.phonetic = Phonetic()
	self.twitterc = TwitterC('twython')
        self.voicesynthetizer = voicesynthetizer

    def setup(self):

        logging.info('Selfie Setup')
        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)
        self.hashtag = self.conf.get("system", "hashtag")

    def get(self):

        logging.info('Selfie Get')
        self.setup()

        try:
            self.camera.pictureCapture()
            media = self.camera.picturePath()
            message = Randomizer(2) + ' ' + self.hashtag + ' #Selfie '
            message = message + 'Voice Infrastructure ... Visit me @ https://github.com/xe1gyq/nuupxe'
            logging.info(message)
            self.twitterc.timeline_set(message, media)
            message = "Hola! Mi selfie en twitter.com/ " + 'nuup x e'
            self.voicesynthetizer.speechit(message)
            message = ' '.join(self.phonetic.decode("nuupxe"))
            self.voicesynthetizer.speechit(message)
        except:
            logging.error('Cannot open Camera device')

        alive(modulename=self.modulename, media=media)

# End of File
