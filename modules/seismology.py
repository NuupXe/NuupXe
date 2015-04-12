#!/usr/bin/python

import re

from core.twitterc import TwitterC

state = {'CHIS': 'Chiapas', 'NL': 'Nuevo Leon', 'VER': 'Veracruz',
	'JAL': 'Jalisco', 'OAX': 'Oaxaca', 'GRO': 'Guerrero',
	'BC': 'Baja California', 'SON': 'Sonora'}

class Seismology(object):

    def __init__(self, voicesynthetizer):

	self.twitterc = TwitterC('twython')

        self.voicesynthetizer = voicesynthetizer

    def SismologicoMX(self):
        print '[NuupXe] Seismology'
        self.voicesynthetizer.speechit('Servicio Sismologico Nacional, Universidad Nacional Autonoma de Mexico')

        tstatus = self.twitterc.timeline_get('SismologicoMX', 1)
        sismo = 'False'
        for status in tstatus:
            if status['text'].partition(' ')[0] == 'SISMO' or status['text'].partition(' ')[0] == 'Preliminar:':
                status['text'] = status['text'].replace("Loc", "Localizacion")
                status['text'] = status['text'].replace("CD", "Ciudad")
                status['text'] = status['text'].replace("Lat", "Latitud")
                status['text'] = status['text'].replace("Lon", "Longitud")
                status['text'] = status['text'].replace("Pf", "Profundidad")
                pattern = re.compile(r'\b(' + '|'.join(state.keys()) + r')\b')
                status['text'] = pattern.sub(lambda x: state[x.group()], status['text'])
                try:
                    self.voicesynthetizer.speechit(status['text'])
                except:
                    print 'Seismology Error'
                sismo = 'True'
        if sismo == 'False':
            self.voicesynthetizer.speechit("No se encontraron sismos en las ultimas horas")

if __name__ == '__main__':

    mytest = SeismologyC("google")
    mytest.sismologicomx()
