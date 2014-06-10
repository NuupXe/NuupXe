#!/usr/bin/python

import ConfigParser
import wolframalpha

from core.morse import Morse
from core.phonetic import Phonetic
from core.voicesynthetizer import VoiceSynthetizer

class Wolfram(object):

    def __init__(self, voicesynthetizer):

        self.phonetic = Phonetic()
        self.voicesynthetizer = voicesynthetizer
        
        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/wolfram.config"
        self.conf.read(self.path)

    def identify(self):
        print '[Cancun] Wolfram'
        appid=self.conf.get("wolfram", "appid")
        client = wolframalpha.Client(appid)
        question = 'how many grams in kilograms'
        res = client.query(question)
        self.voicesynthetizer.speechit(question)
        print(next(res.results).text)
        self.voicesynthetizer.speechit(next(res.results).text)

if __name__ == '__main__':

    mytest = Wolfram()
    mytest.identify()
