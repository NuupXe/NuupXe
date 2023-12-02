#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from core.alive import alive
from core.twitterc import TwitterC

state = {'CHIS': 'Chiapas', 'NL': 'Nuevo Leon', 'VER': 'Veracruz',
	'JAL': 'Jalisco', 'OAX': 'Oaxaca', 'GRO': 'Guerrero',
	'BC': 'Baja California', 'SON': 'Sonora', 'RT': 'Retweet'}

class Seismology(object):

    def __init__(self, voicesynthetizer):

        self.modulename = 'Seismology'
        self.twitterc = TwitterC('twython')
        self.voicesynthetizer = voicesynthetizer

    def SismologicoMX(self):
        print('[NuupXe] Seismology')
        message = 'Servicio Sismologico '

        tstatus = self.twitterc.timeline_get('skyalertmx', 3)
        sismo = 'False'
        for status in tstatus:
            if not status['text'].partition(' ')[0] == 'SISMO' or not status['text'].partition(' ')[0] == 'Preliminar:':
                status['text'] = status['text']
                status['text'] = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', status['text'])
                URLless_string = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', status['text'])
                status['text'] = status['text'].replace("Loc", "Localizacion")
                status['text'] = status['text'].replace("CD", "Ciudad")
                status['text'] = status['text'].replace("Lat", "Latitud")
                status['text'] = status['text'].replace("Lon", "Longitud")
                status['text'] = status['text'].replace("Pf", "Profundidad")
                status['text'] = status['text'].replace("SSN", "Servicio Sismologico Nacional")
                pattern = re.compile(r'\b(' + '|'.join(state.keys()) + r')\b')
                status['text'] = pattern.sub(lambda x: state[x.group()], status['text'])
                try:
                    message = message + status['text']
                except:
                    print('Seismology Error')
                sismo = 'True'
        if sismo == 'False':
            self.voicesynthetizer.speechit("No se encontraron sismos en las ultimas horas")
        else:
            self.voicesynthetizer.speechit(message)
            alive(modulename=self.modulename, modulemessage=message)

# End of File
