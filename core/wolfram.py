#!/usr/bin/python

import configparser
import logging
import re
import wolframalpha

class Wolfram(object):

    def __init__(self):

        logging.info('Wolfram')
        self.conf = configparser.ConfigParser()
        self.path = "configuration/services.config"
        self.conf.read(self.path)
        appid=self.conf.get("wolfram", "appid")
        self.client = wolframalpha.Client(appid)

    def question(self, question):
        logging.info('Wolfram Question')
        logging.info("Wolfram Alpha Experimental Module, Computational Knowledge Engine")
        try:
            res = self.client.query(question)
            logging.info((next(res.results).text))
            string = re.sub('[^0-9a-zA-Z]+', ' ', next(res.results).text)
            logging.info(string)
            return string
        except:
            logging.info('Wolfram Question Error in Client Query')
            return None

# End of File
