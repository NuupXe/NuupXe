#!/usr/bin/python

import codecs
import ConfigParser
import logging
import time
import sys

from datetime import date

from core.alive import alive
from core.morse import Morse
from core.phonetic import Phonetic
from core.voicesynthetizer import VoiceSynthetizer

class Messages(object):

    def __init__(self, voicesynthetizer):

        self.modulename = 'Messages'
        self.morse = Morse()
        self.speaker = voicesynthetizer
        self.phonetic = Phonetic()

    def message(self, message):
        if self.speaker.getsynthetizer() == "google":
            message = "\"" + message + "\""
        self.speaker.speechit(message)
        time.sleep(1)

    def readfile(self, textfile):

        print '[NuupXe] Messages: Voice to Speech Text File'

        file = codecs.open(textfile)
        for line in file.readlines():
            if "pausa" in line:
                self.message("Hagamos una Pausa de 1 minuto")
                time.sleep(60)
                self.message("Continuamos")
            else:
                self.message(line)
        return

    def stations(self):

	print '[NuupXe] Messages: Stations'

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/stations.config"
        self.conf.read(self.path)

        city = self.conf.get('general', 'city')
        self.speaker.speechit("Lista de Repetidores y Estaciones en la ciudad de " + city)
        self.conf.remove_section('general')

        for section in self.conf.sections():

            try:

                type = self.conf.get(section, 'type')
                owner = self.conf.get(section, 'owner')
                callsign = self.conf.get(section, 'callsign')
                frequency = self.conf.get(section, 'frequency')
                subtone = self.conf.get(section, 'subtone')

                self.morse.generate(callsign)
                station = type + ' ' + callsign
                stationdecoded = type + ' ' + ' '.join(self.phonetic.decode(callsign))
                message = ", Propietario " + owner
                messagex = ", Propietario " + owner
                message = message + ", Frecuencia " +  '.'.join(frequency.split('.'))
                messagex = messagex + ", Frecuencia " +  frequency
                message = message + ", Subtono " + ' '.join(self.phonetic.decode(subtone))
                messagex = messagex + ", Subtono " + subtone

                sign = self.conf.get(section, 'sign')
                offset = self.conf.get(section, 'offset')

                if sign == 'simplex':
                    message = message + ", Offset " + sign
                    messagex = messagex + ", Offset " + sign
                else:
                    message = message + ", Offset " + ' '.join(self.phonetic.decode(sign)) + " " + offset
                    messagex = messagex + ", Offset " + sign + " " + offset

                modulemessage = station + messagex
                speechmessage = stationdecoded + message
                self.speaker.speechit(speechmessage)
                alive(modulename=self.modulename, modulemessage=modulemessage)
                time.sleep(2)

            except:

                logging.error(self.modulename + 'Error Stations')

