#!/usr/bin/python

import commands
import ConfigParser
import logging

from core.alive import Alive
from core.pushtotalk import PushToTalk

class SSTV(object):

    def __init__(self, voicesynthetizer):

        self.modulename = 'SSTV'
        self.modulepicture = 'output/radioclub.jpg'
        self.voicesynthetizer = voicesynthetizer
        self.pushtotalk = PushToTalk()

    def setup(self):

        logging.info('SSTV Setup')

    def alive(self):
        self.alive = Alive()
        self.alive.report(self.modulename, self.modulepicture)

    def decode(self):

        logging.info('SSTV Decode')
        self.setup()
        try:
            status, output = commands.getstatusoutput('python core/bing.py')
            status, output = commands.getstatusoutput('convert -resize 320x256\! output/bing.jpg output/radioclub.jpg')
            status, output = commands.getstatusoutput('python -m pysstv --mode MartinM1 --vox output/radioclub.jpg output/sstv.wav')
            self.voicesynthetizer.speechit("Modulo Experimental de Television de Barrido Lento, Modo Martin Uno")
            self.pushtotalk.openport()
            status, output = commands.getstatusoutput('aplay output/sstv.wav')
            self.pushtotalk.closeport()
            self.alive()
        except:
            logging.error('Cannot decode file')

# End of File
