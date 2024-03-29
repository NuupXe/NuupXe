#!/usr/bin/python

import threading
from time import sleep
import re

from core.twitterc import TwitterC
from core.voicerecognition import VoiceRecognition
from core.voicesynthesizer import VoiceSynthesizer

from modules.voicemail import VoiceMail
from modules.clock import Clock
from modules.identification import Identification
from modules.weather import Weather
from modules.messages import Messages
from modules.seismology import Seismology

def main(voicesynthetizer):

    voicesynthetizer = voicesynthetizer
    t = Assistante(voicesynthetizer)
    t.go()
    try:
        join_threads(t.threads)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt catched.")
        print("Terminate main thread.")
        print("If only daemonic threads are left, terminate whole program.")

class Assistant(object):

    def __init__(self, voicesynthetizer):

        self.modulename = 'Assistant'
        self.running = True
        self.introduced = False
        self.threads = []
        self.voicesynthetizer = voicesynthetizer

        self.voicerecognition = VoiceRecognition(self.voicesynthetizer)
        self.voicemail = VoiceMail(self.voicesynthetizer)
        self.clock = Clock(voicesynthetizer)
        self.identification = Identification(voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.seismology = Seismology(self.voicesynthetizer)

    def demo1(self):
        self.introduction1()
        self.command()

    def demo2(self):
        self.introduction2()
        self.command()

    def introduction1(self):
        self.voicesynthetizer.speechit("Hola! Dime como puedo ayudarte?")
        self.introduced = True

    def introduction2(self):
        while True:
            self.voicerecognition.record('5')
            output = self.voicerecognition.recognize('False')
            if re.search(r'hola', output, re.M|re.I) or re.search(r'nu', output, re.M|re.I):
                self.voicesynthetizer.speechit("Hola! Dime como puedo ayudarte?")
                self.introduced = True
                break

    def command(self):
        while self.introduced:
            self.voicerecognition.record()
            output = self.voicerecognition.recognize('False')
            if re.search(r'identif', output, re.M|re.I):
                print('[NuupXe] Assistant Identification')
                self.identification.identify()
            elif re.search(r'hora', output, re.M|re.I) or re.search(r'ora', output, re.M|re.I) :
                print('[NuupXe] Assistant Hour')
                self.clock.hour()
            elif re.search(r'fecha', output, re.M|re.I):
                print('[NuupXe] Assistant Date')
                self.clock.date()
            elif re.search(r'reporte', output, re.M|re.I) or re.search(r'clima', output, re.M|re.I):
                print('[NuupXe] Assistant Weather')
                self.weather.report()
            elif re.search(r'estaciones', output, re.M|re.I) or re.search(r'repetidores', output, re.M|re.I):
                print('[NuupXe] Assistant Stations')
                self.messages.stations()
            elif re.search(r'sismo', output, re.M|re.I):
                print('[NuupXe] Assistant Seismic')
                self.seismology.SismologicoMX()
            elif re.search(r'mensaje', output, re.M|re.I) or re.search(r'avis', output, re.M|re.I):
                print('[NuupXe] Assistant Message')
                if self.voicemail.status:
                    self.voicesynthetizer.speechit("Mensaje existente!")
                    while True:
                        self.voicesynthetizer.speechit("Quieres escucharlo, borrarlo o salir de esta opcion")
                        self.voicerecognition.record()
                        output = self.voicerecognition.recognize('False')
                        if re.search(r'escuchar', output, re.M|re.I):
                            print('[NuupXe] Assistant Message Play')
                            self.voicemail.play()
                        elif re.search(r'borrar', output, re.M|re.I):
                            print('[NuupXe] Assistant Message Erase')
                            self.voicemail.erase()
                        elif re.search(r'salir', output, re.M|re.I):
                            print('[NuupXe] Assistant Message Quit')
                            self.voicesynthetizer.speechit("Saliendo de Opcion Mensaje")
                            break
                        else:
                            self.voicemail.record()
                            self.voicemail.play()
                elif re.search(r'dormir', output, re.M|re.I):
                    print('[NuupXe] Assistant Sleep')
                    self.voicesynthetizer.speechit("Perfecto! Gracias! Dormire por los proximos 30 segundos")
                    sleep(30)
                    self.voicesynthetizer.speechit("Ya desperte! Que rica siesta!")
                elif re.search(r'eventos', output, re.M|re.I):
                    print('[NuupXe] Assistant Bye')
                    self.voicesynthetizer.speechit("El radioclub tiene 2 eventos proximos")
                    self.voicesynthetizer.speechit("Boletin Tecnologico, Miercoles, 8:00 pm")
                    self.voicesynthetizer.speechit("Junta Mensual, Jueves 8:00 pm, recuerda traer galletas")
                elif re.search(r'nada', output, re.M|re.I) or re.search(r'dios', output, re.M|re.I) or re.search(r'ativo', output, re.M|re.I):
                    print('[NuupXe] Assistant Bye')
                    self.voicesynthetizer.speechit("Hasta pronto!")
                    self.running = False
                    break
                else:
                    print('[NuupXe] Assistant? Unknown!')

                self.voicesynthetizer.speechit("Se ofrece algo mas?")

    def foo(self):
        while(self.running):
            print('[NuupXe] Assistante | Foo Hello')
            sleep(5)

    def get_user_input(self):
        while True:
            x = raw_input("Tupe any text, Enter 'e' for exit: ")
            if x.lower() == 'e':
               self.running = False
               break
            else:
               self.voicesynthetizer.speechit(x)

    def twitter(self):
        return
        self.twitterc = TwitterC('twython')
        self.oldstatus = ''
        self.newstatus = ''
	
        while (self.running):
            print('[NuupXe] Assistante | Twitter Hello')
	    #self.voicesynthetizer.speechit("Veamos")
            tstatus = self.twitterc.timeline_get('xe1gyq', 1)
            for status in tstatus:
                self.newstatus = status['text']
                if self.newstatus != self.oldstatus:
                    self.oldstatus = self.newstatus
                    self.voicesynthetizer.speechit("Nuevo mensaje en cuenta de Twitter!")
                    self.voicesynthetizer.speechit(self.newstatus)
            sleep(5)

    def go(self):
        t1 = threading.Thread(target=self.foo)
        t2 = threading.Thread(target=self.get_user_input)
        t3 = threading.Thread(target=self.twitter)
        t4 = threading.Thread(target=self.demo1)
        # Make threads daemonic, i.e. terminate them when main thread
        # terminates. From: http://stackoverflow.com/a/3788243/145400
        t1.daemon = True
        t2.daemon = True
        t3.daemon = True
        t4.daemon = True
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        self.threads.append(t1)
        self.threads.append(t2)
        self.threads.append(t3)
        self.threads.append(t4)


def join_threads(threads):
    """
    Join threads in interruptable fashion.
    From http://stackoverflow.com/a/9790882/145400
    """
    for t in threads:
        while t.isAlive():
            t.join(5)

# Enf of File
