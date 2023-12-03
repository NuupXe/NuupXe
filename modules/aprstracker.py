#!/usr/bin/python

import configparser
import feedparser
import geocoder
import logging
import os
import string
import sys
import time
import unicodedata

from core.alive import alive

from core.aprsfi import AprsFi
from core.voicesynthesizer import VoiceSynthesizer
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

    def __init__(self, voicesynthetizer, callsign='XE1GYP-9'):
        logging.info('[AprsTracker]')
        self.speaker = voicesynthetizer
        self.callsign = callsign
        self.modulename = 'AprsTracker'

        self.phonetic = Phonetic()
        self.aprsfi = AprsFi()

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

    def time(self, aprstime):
        logging.info('[AprsTracker] Time')
        weekday = days[time.strftime("%A", time.gmtime(int(aprstime)))]
        day = time.strftime("%d", time.gmtime(int(aprstime))).lstrip('0')
        month = months[time.strftime("%B", time.gmtime(int(aprstime)))]
        year = time.strftime("%Y", time.gmtime(int(aprstime)))
        return weekday, day, month, year

    def localize(self):
        logging.info('[AprsTracker] Localize')
        self.speaker.speechit("Localizacion de estaciones a traves de a p r s punto f i")
        self.aprsfi.callsignset(self.callsign)
        self.aprsfi.dataset('loc')
        data = self.aprsfi.query()
        logging.info(data)

        station = "Estacion " + self.callsign
        stationdecoded = "Estacion " + ' '.join(self.phonetic.decode(self.callsign))

        if data.get('entries'):
            for entry in data['entries']:
                weekday, day, month, year = self.time(entry['lasttime'])
                message = ", Ultima vez visto " + weekday + ' ' + day + ' de ' + month + ' del ' + year
                try:
                    message =  message + ", Velocidad " + str(entry['speed']) + " Km/h"
                except:
                    pass
                try:
                    message =  message + ", Altitud " + str(entry['altitude']) + " metros"
                except:
                    pass
                results = geocoder.osm(float(entry['lat']), float(entry['lng']))
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

                speechmessage = stationdecoded + message
                self.speaker.speechit(speechmessage)

            modulemessage = station + message
            alive(modulename=self.modulename, modulemessage=modulemessage)

        else:
            self.speaker.speechit(stationdecoded + " no ha reportado ubicacion!")

# End of File
