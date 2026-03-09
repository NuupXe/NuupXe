#!/usr/bin/python

import threading
from time import sleep
import re

from core.voicerecognition import VoiceRecognition

from modules.voicemail import VoiceMail
from modules.clock import Clock
from modules.identification import Identification
from modules.weather import Weather
from modules.messages import Messages
from modules.seismology import Seismology


def main(voicesynthesizer):
    t = Assistant(voicesynthesizer)
    t.go()
    try:
        join_threads(t.threads)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt catched.")
        print("Terminate main thread.")

class Assistant(object):

    def __init__(self, voicesynthesizer):

        self.modulename = 'Assistant'
        self.running = True
        self.introduced = False
        self.threads = []
        self.voicesynthesizer = voicesynthesizer

        self.voicerecognition = VoiceRecognition(self.voicesynthesizer)
        self.voicemail = VoiceMail(self.voicesynthesizer)
        self.clock = Clock(voicesynthesizer)
        self.identification = Identification(voicesynthesizer)
        self.weather = Weather(self.voicesynthesizer)
        self.messages = Messages(self.voicesynthesizer)
        self.seismology = Seismology(self.voicesynthesizer)

    def demo1(self):
        self.introduction1()
        self.command()

    def demo2(self):
        self.introduction2()
        self.command()

    def introduction1(self):
        self.voicesynthesizer.speech_it("Hola! Dime como puedo ayudarte?")
        self.introduced = True

    def introduction2(self):
        while True:
            self.voicerecognition.record('5')
            output = self.voicerecognition.recognize('False')
            if re.search(r'hola', output, re.M|re.I) or re.search(r'nu', output, re.M|re.I):
                self.voicesynthesizer.speech_it("Hola! Dime como puedo ayudarte?")
                self.introduced = True
                break

    def command(self):
        while self.introduced:
            self.voicerecognition.record()
            output = self.voicerecognition.recognize('False')
            if re.search(r'identif', output, re.M|re.I):
                print('[NuupXe] Assistant Identification')
                self.identification.identify()
            elif re.search(r'hora', output, re.M|re.I) or re.search(r'ora', output, re.M|re.I):
                print('[NuupXe] Assistant Hour')
                self.clock.hour()
            elif re.search(r'fecha', output, re.M|re.I):
                print('[NuupXe] Assistant Date')
                self.clock.date()
            elif re.search(r'reporte', output, re.M|re.I) or re.search(r'clima', output, re.M|re.I):
                print('[NuupXe] Assistant Weather')
                self.weather.weather_report()
            elif re.search(r'estaciones', output, re.M|re.I) or re.search(r'repetidores', output, re.M|re.I):
                print('[NuupXe] Assistant Stations')
                self.messages.stations()
            elif re.search(r'sismo', output, re.M|re.I):
                print('[NuupXe] Assistant Seismic')
                self.seismology.SismologicoMX()
            elif re.search(r'mensaje', output, re.M|re.I) or re.search(r'avis', output, re.M|re.I):
                print('[NuupXe] Assistant Message')
                self.voicesynthesizer.speech_it("Quieres grabar o escuchar un mensaje?")
                self.voicerecognition.record()
                output = self.voicerecognition.recognize('False')
                if re.search(r'escuchar', output, re.M|re.I):
                    print('[NuupXe] Assistant Message Play')
                    self.voicemail.play()
                elif re.search(r'grabar', output, re.M|re.I):
                    print('[NuupXe] Assistant Message Record')
                    self.voicemail.record()
                    self.voicemail.play()
                elif re.search(r'salir', output, re.M|re.I):
                    self.voicesynthesizer.speech_it("Saliendo de Opcion Mensaje")
            elif re.search(r'dormir', output, re.M|re.I):
                print('[NuupXe] Assistant Sleep')
                self.voicesynthesizer.speech_it("Perfecto! Gracias! Dormire por los proximos 30 segundos")
                sleep(30)
                self.voicesynthesizer.speech_it("Ya desperte! Que rica siesta!")
            elif re.search(r'eventos', output, re.M|re.I):
                print('[NuupXe] Assistant Events')
                self.voicesynthesizer.speech_it("El radioclub tiene 2 eventos proximos")
                self.voicesynthesizer.speech_it("Boletin Tecnologico, Miercoles, 8:00 pm")
                self.voicesynthesizer.speech_it("Junta Mensual, Jueves 8:00 pm, recuerda traer galletas")
            elif re.search(r'nada', output, re.M|re.I) or re.search(r'dios', output, re.M|re.I) or re.search(r'ativo', output, re.M|re.I):
                print('[NuupXe] Assistant Bye')
                self.voicesynthesizer.speech_it("Hasta pronto!")
                self.running = False
                break
            else:
                print('[NuupXe] Assistant? Unknown!')

            self.voicesynthesizer.speech_it("Se ofrece algo mas?")

    def foo(self):
        while self.running:
            print('[NuupXe] Assistant | Foo Hello')
            sleep(5)

    def get_user_input(self):
        while True:
            x = input("Type any text, Enter 'e' for exit: ")
            if x.lower() == 'e':
                self.running = False
                break
            else:
                self.voicesynthesizer.speech_it(x)

    def go(self):
        t1 = threading.Thread(target=self.foo)
        t2 = threading.Thread(target=self.get_user_input)
        t3 = threading.Thread(target=self.demo1)
        t1.daemon = True
        t2.daemon = True
        t3.daemon = True
        t1.start()
        t2.start()
        t3.start()
        self.threads.append(t1)
        self.threads.append(t2)
        self.threads.append(t3)


def join_threads(threads):
    for t in threads:
        while t.is_alive():
            t.join(5)

# End of File
