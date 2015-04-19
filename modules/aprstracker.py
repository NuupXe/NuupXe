#!/usr/bin/python

import ConfigParser
import feedparser
import logging
import os
import pywapi
import string
import sys
import time
import unicodedata

from core.alive import alive

from pygeocoder import Geocoder
from core.aprsfi import AprsFi
from core.voicesynthetizer import VoiceSynthetizer
from core.phonetic import Phonetic

days = {'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miercoles',
'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sabado',
'Sunday': 'Domingo',
}

months = {'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
'October': 'Octubre', 'November' : 'Noviembre', 'December': 'Diciembre'
}

class AprsTracker(object):

    def __init__(self, voicesynthetizer):

        self.modulename = 'AprsTracker'
        self.phonetic = Phonetic()
        self.aprsfi = AprsFi()

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

        self.speaker = voicesynthetizer
        self.callsign = 'XE1GQP-9'

    def clock(self, aprstime):

        logging.info('Aprs Tracker Clock')
        weekday = days[time.strftime("%A", time.gmtime(int(aprstime)))]
        day = time.strftime("%d", time.gmtime(int(aprstime))).lstrip('0')
        month = months[time.strftime("%B", time.gmtime(int(aprstime)))]
        year = time.strftime("%Y", time.gmtime(int(aprstime)))
        return weekday, day, month, year

    def query(self):

        logging.info('Aprs Tracker Query')
        self.speaker.speechit("Localizacion de estaciones a traves de a p r s punto f i")
        self.localize(self.callsign)

    def localize(self, callsign):

        self.aprsfi.callsignset(callsign)
        self.aprsfi.dataset('loc')
        data = self.aprsfi.query()
        logging.info(data)

        for entry in data['entries']:
            message = ", Estacion " + ' '.join(self.phonetic.decode(callsign))
            weekday, day, month, year = self.clock(entry['lasttime'])
            message = message + ", Ultima vez visto " + weekday + ' ' + day + ' de ' + month + ' del ' + year
            try:
                message =  message + ", Velocidad " + str(entry['speed']) + " Km/h"
            except:
                pass
            try:
                message =  message + ", Altitud " + str(entry['altitude']) + " metros"
            except:
                pass
            results = Geocoder.reverse_geocode(float(entry['lat']), float(entry['lng']))
            logging.info(results)
            try:
                message = message + ", Calle " + results[0].route
                message = message + ", Colonia " + results[0].political
                if results[0].administrative_area_level_2:
                    message = message + ", Municipio " + results[0].administrative_area_level_2
                elif results[0].locality:
                    message =  message + ", Municipio " + results[0].locality
                message =  message + ", " + results[0].administrative_area_level_1
                message =  message + ", " + results[0].country
            except:
                pass
            self.speaker.speechit(message)

        alive(self.modulename)


# End of File
