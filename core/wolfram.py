#!/usr/bin/python

import ConfigParser
import logging
import re
import wolframalpha

class Wolfram(object):

    def __init__(self, voicesynthetizer):

        self.voicesynthetizer = voicesynthetizer
        
    def setup(self):
        logging.info('Wolfram Setup')
        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/services.config"
        self.conf.read(self.path)
        appid=self.conf.get("wolfram", "appid")
        self.client = wolframalpha.Client(appid)

    def question(self, question):
        logging.info('Wolfram Question')
        self.setup()
        self.voicesynthetizer.setlanguage("english")
        logging.info("Wolfram Alpha Experimental Module, Computational Knowledge Engine")
        res = self.client.query(question)
        self.voicesynthetizer.speechit(question)
        logging.info((next(res.results).text))
        string = re.sub('[^0-9a-zA-Z]+', ' ', next(res.results).text)
        logging.info(string)
        self.voicesynthetizer.speechit(string)
        self.voicesynthetizer.setlanguage("spanish")

# End of File
