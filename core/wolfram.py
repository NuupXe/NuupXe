#!/usr/bin/python

import ConfigParser
import re
import wolframalpha

from core.voicesynthetizer import VoiceSynthetizer

class Wolfram(object):

    def __init__(self, voicesynthetizer):

        self.voicesynthetizer = voicesynthetizer
        
        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/services.config"
        self.conf.read(self.path)
        self.questions = [
        'what is the population in Mexico',
        'how far is mexico from the US']

    def identify(self):
        print '[Cancun] Wolfram'
        appid=self.conf.get("wolfram", "appid")
        self.client = wolframalpha.Client(appid)

    def question(self, question):
        self.identify()
        self.voicesynthetizer.setlanguage("english")
        self.voicesynthetizer.speechit("Wolfram Alpha Experimental Module, Computational Knowledge Engine")
        for question in self.questions:
                res = self.client.query(question)
                self.voicesynthetizer.speechit(question)
                print(next(res.results).text)
                string = re.sub('[^0-9a-zA-Z]+', ' ', next(res.results).text)
                print string
                self.voicesynthetizer.speechit(string)
        self.voicesynthetizer.setlanguage("spanish")

if __name__ == '__main__':

    mytest = Wolfram()
    mytest.identify()
