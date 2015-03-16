#!/usr/bin/python

import ConfigParser
import json
import urllib2

class AprsFi(object):

    def __init__(self):

        self.configuration()

        self.callsign = None
        self.data = None

    def configuration(self):
        self.conf = ConfigParser.ConfigParser()
        self.services = "configuration/services.config"
        self.conf.read(self.services)
        self.api_key = self.conf.get("aprsfi", "api_key")

    def callsignset(self, callsign):
        self.callsign = callsign

    def dataset(self, data):
        self.data = data

    def query(self):
        try:
            url = 'http://api.aprs.fi/api/get?name=' + self.callsign + '&what=' + self.data + '&apikey=' + self.api_key + '&format=json'
            data = json.loads(urllib2.urlopen(url).read())
            return data
        except:
            print '[Cancun] AprsFi | Query Error'

# End of File
