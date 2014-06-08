#!/usr/bin/python

import ConfigParser
import wolframalpha

from core.morse import Morse
from core.phonetic import Phonetic
from core.voicesynthetizer import VoiceSynthetizer

class Wolfram(object):

    def __init__(self, voicesynthetizer):

        self.phonetic = Phonetic()
        self.voicesynthetizer = VoiceSynthetizer("google", "english")
        
        self.conf = ConfigParser.ConfigParser()
        self.path = "../configuration/wolfram.config"
        self.conf.read(self.path)

    def identify(self):
        print '[Cancun] Wolfram'
        appid=self.conf.get("wolfram", "appid")
	client = wolframalpha.Client(appid)
	res = client.query('how many words can someone say in one day')
	print(next(res.results).text)
        self.voicesynthetizer.speechit(next(res.results).text)

if __name__ == '__main__':

    mytest = Wolfram("google")
    mytest.identify()
