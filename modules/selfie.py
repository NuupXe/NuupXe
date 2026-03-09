#!/usr/bin/python

import configparser
import logging
import random

from core.alive import alive
from core.camera import Camera
from core.phonetic import Phonetic
from core.twitterc import TwitterC
from core.utilities import Randomizer

class Selfie(object):

    def __init__(self, voicesynthesizer):

        self.modulename = 'Selfie'
        self.camera = Camera(voicesynthesizer)
        self.phonetic = Phonetic()
        self.twitterc = TwitterC('twython')
        self.voicesynthesizer = voicesynthesizer

    def setup(self):

        logging.info('Selfie Setup')
        self.conf = configparser.ConfigParser()
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
            self.voicesynthesizer.speech_it(message)
            message = ' '.join(self.phonetic.decode("nuupxe"))
            self.voicesynthesizer.speech_it(message)
        except:
            logging.error('Cannot open Camera device')

        alive(modulename=self.modulename, media=media)

# End of File
