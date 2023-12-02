#!/usr/bin/python

import configparser
import json
import logging
import urllib


class AprsFi(object):

    def __init__(self, callsign=None, data=None):
        logging.info('[AprsFi]')
        self.callsign = callsign
        self.data = data
        self.conf = ConfigParser.ConfigParser()
        self.services = "configuration/services.config"
        self.conf.read(self.services)
        self.api_key = self.conf.get("aprsfi", "api_key")

    def callsignset(self, callsign):
        logging.info('[AprsFi] CallsignSet')
        self.callsign = callsign

    def callsignget(self, callsign):
        logging.info('[AprsFi] CallsignGet')
        return self.callsign

    def dataset(self, data):
        logging.info('[AprsFi] DataSet')
        self.data = data

    def dataget(self, data):
        logging.info('[AprsFi] DataGet')
        return self.data

    def query(self):
        logging.info('[AprsFi] Query')
        try:
            url = 'http://api.aprs.fi/api/get?name=' + \
                  self.callsign + '&what=' + \
                  self.data + '&apikey=' + \
                  self.api_key + '&format=json'
            result = json.loads(urllib.urlopen(url).read())
            return result
        except:
            logging.info('[AprsFi] Query Error')

# End of File
