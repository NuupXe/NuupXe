#!/usr/bin/python

from core.twitterc import TwitterC

city = {'CHIS': 'Chiapas', 'NL': 'Nuevo Leon', 'VER': 'Veracurz',
	'JAL': 'Jalisco', 'OAX': 'Oaxaca'}

class Seismology(object):

    def __init__(self, voicesynthetizer):

	self.twitterc = TwitterC()

        self.voicesynthetizer = voicesynthetizer


    def SismologicoMX(self):
        print '[Cancun] Seismology'
        self.voicesynthetizer.speechit('Servicio Sismologico Nacional, Universidad Nacional Autonoma de Mexico')

        tstatus = self.twitterc.user('SismologicoMX')
        sismo = 'False'
        for status in tstatus:
            if status.text.partition(' ')[0] == 'SISMO':
                    status.text = status.text.replace("Loc", "Localizacion")
                    status.text = status.text.replace("CD", "Ciudad")
                    status.text = status.text.replace("Lat", "Latitud")
                    status.text = status.text.replace("Lon", "Longitud")
                    status.text = status.text.replace("Pf", "Profundidad")
                    self.voicesynthetizer.speechit(status.text)
                    sismo = 'True'
        if sismo == 'False':
                    self.voicesynthetizer.speechit("No se encontraron sismos en las ultimas horas")

if __name__ == '__main__':

    mytest = SeismologyC("google")
    mytest.sismologicomx()
