#!/usr/bin/python

import codecs
import ConfigParser
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

        self.sections = self.conf.sections()
        for section in self.sections:

            try:
                type = self.conf.get(section, 'type')           
                owner = self.conf.get(section, 'owner')
                callsign = self.conf.get(section, 'callsign')
                frequency = self.conf.get(section, 'frequency')
                subtone = self.conf.get(section, 'subtone')

                self.speaker.speechit(type + ", " + ' '.join(self.phonetic.decode(callsign)))
                self.morse.generate(callsign)
                self.speaker.speechit("Propietario, " + owner)
                self.speaker.speechit("Frecuencia, " +  ', '.join(frequency.split('.')))
                self.speaker.speechit("Subtono, " +  ' '.join(self.phonetic.decode(subtone)))

                sign = self.conf.get(section, 'sign')
                offset = self.conf.get(section, 'offset')
                
                if sign == 'simplex':
                    self.speaker.speechit("Offset, " + sign)
                else:
                    self.speaker.speechit("Offset, " + ' '.join(self.phonetic.decode(sign)) + " " + offset) 

                time.sleep(2)

            except:

                None

        alive(self.modulename)
