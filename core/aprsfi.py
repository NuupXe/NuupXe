#!/usr/bin/python

import ConfigParser
import commands
import json
import time
import os
import urllib2

class AprsFi(object):

    def __init__(self):

        self.conf = ConfigParser.ConfigParser()
        self.services = "configuration/services.config"
        self.conf.read(self.services)
        self.api_key = self.conf.get("aprsfi", "api_key")

        self.callsign = None
        self.data = None

    def callsign_set(self, callsign):
        self.callsign = callsign

    def data_set(self, data):
        self.data = data

    def query(self):
        url = 'http://api.aprs.fi/api/get?name=' + self.callsign + '&what=' + self.data + '&apikey=' + self.api_key + '&format=json'
        data = json.loads(urllib2.urlopen(url).read())
        return data

if __name__ == '__main__':

    mytest = AprsFi()
