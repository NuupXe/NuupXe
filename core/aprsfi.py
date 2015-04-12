#!/usr/bin/python

import ConfigParser
import json
import logging
import urllib2

class AprsFi(object):

    def __init__(self):

        self.callsign = None
        self.data = None

        self.configuration()

    def configuration(self):
        logging.info('[NuupXe] AprsFi Configuration')
        self.conf = ConfigParser.ConfigParser()
        self.services = "configuration/services.config"
        self.conf.read(self.services)
        self.api_key = self.conf.get("aprsfi", "api_key")

    def callsignset(self, callsign):
        logging.info('[NuupXe] AprsFi CallsignSet')
        self.callsign = callsign

    def dataset(self, data):
        logging.info('[NuupXe] AprsFi DataSet')
        self.data = data

    def query(self):
        logging.info('[NuupXe] AprsFi Query')
        try:
            url = 'http://api.aprs.fi/api/get?name=' + self.callsign + '&what=' + self.data + '&apikey=' + self.api_key + '&format=json'
            data = json.loads(urllib2.urlopen(url).read())
            return data
        except:
            logging.info('[NuupXe] AprsFi Query Error')

# End of File
