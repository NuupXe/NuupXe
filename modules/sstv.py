#!/usr/bin/python

import commands
import ConfigParser
import logging

from core.pushtotalk import PushToTalk

class SSTV(object):

    def __init__(self, voicesynthetizer):

        self.voicesynthetizer = voicesynthetizer
        self.pushtotalk = PushToTalk()

    def setup(self):

        logging.info('SSTV Setup')

    def decode(self):

        logging.info('SSTV Decode')
        self.setup()
        self.voicesynthetizer.speechit("Modulo Experimental de Television de Barrido Lento, Modo Robot 36")
        try:
            #status, output = commands.getstatusoutput('python -m pysstv --mode Robot36 output/craeg.jpg output/sstv.wav')
            self.pushtotalk.openport()
            status, output = commands.getstatusoutput('aplay output/sstv.wav')
            self.pushtotalk.closeport()
        except:
            logging.error('Cannot decode file')

# End of File
