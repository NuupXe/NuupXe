import configparser
import time
from pyowm import OWM

from core.alive import alive
from core.aprsnet import AprsNet
from core.aprsfi import AprsFi
from core.voicesynthesizer import VoiceSynthesizer
from core.phonetic import Phonetic

class Weather(object):

    def __init__(self, voicesynthesizer):
        self.modulename = 'Weather'
        self.phonetic = Phonetic()
        self.aprsfi = AprsFi()

        self.conf = configparser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

        self.agent = self.conf.get("weather", "agent")
        self.location = self.conf.get("weather", "location")
        self.speaker = voicesynthesizer

    def aprspacket(self):
        self.aprsnet = AprsNet()
        self.aprsnet.send_packet("XE1GYQ-13>APRS,TCPIP*,qAS,XE1GYQ-10:@232353z2036.96N/10324.58W_000/000g000t000r000p000P000h00b00000NuupXe Weather Station")

    def aprsfi_service(self):
        print('[NuupXe] Weather aprs.fi')
        callsign = self.conf.get("weather", "aprsficallsign")
        location = self.conf.get("weather", "aprsfilocation")

        self.aprsfi.callsignset(callsign)
        self.aprsfi.dataset('wx')
        data = self.aprsfi.query()

        for entry in data['entries']:
            message = f"Reporte del clima en la ciudad de {location}, Datos de aprs.fi, \
                        Estacion meteorologica, {' '.join(self.phonetic.decode(callsign))}, \
                        Temperatura {entry['temp']} grados centigrados, \
                        Humedad relativa {entry['humidity']} por ciento, \
                        Presion Atmosferica {entry['pressure']} milibares, \
                        Direccion del viento {entry['wind_direction']} grados, \
                        Velocidad del viento {entry['wind_speed']} metros por segundo, \
                        Rafagas de {entry['wind_gust']} metros por segundo, \
                        Precipitacion pluvial {entry['rain_1h']} milimetros"
            self.speaker.speech_it(message)
            self.message = message

    def openweathermap(self):
        print('[NuupXe] Open Weather Map')

        services = configparser.ConfigParser()
        path = "configuration/services.config"
        services.read(path)
        owmkey = services.get("openweathermap", "key")

        owm = OWM(owmkey)
        city = self.conf.get("general", "location")

        try:
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place("Tlaquepaque, Mexico")
            w = observation.weather
        except Exception as e:
            print(f"An error occurred: {e}")

        message = f"Reporte del Clima promedio en {city}, \
                    Temperatura {w.temperature('celsius')['temp']} grados centigrados, \
                    Presion Atmosferica {w.pressure['press']} milibares, \
                    Humedad {w.humidity} por ciento, Nubosidad {w.clouds} por ciento, \
                    El Sol se oculta a las {time.strftime('%H:%M', time.localtime(int(w.sunset_time('unix'))))}"
        self.speaker.speech_it(message)
        self.message = message

    def weather_report(self):
        print(self.agent)

        if self.agent == "aprsfi":
            self.aprsfi_service()
        elif self.agent == "openweathermap":
            self.openweathermap()

        self.aprspacket()
        # alive(modulename=self.modulename + 'Report', modulemessage=self.message)

    def weather_temperature(self):
        services = configparser.ConfigParser()
        path = "configuration/services.config"
        services.read(path)
        owmkey = services.get("openweathermap", "key")

        owm = OWM(owmkey)
        idioma = 'es'
        location = self.location

        try:
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(str(location))
            w = observation.weather
        except Exception as e:
            print(f"An error occurred: {e}")

        _detailed_status = w.detailed_status
        _temperature = str(w.temperature('celsius')['temp'])

        message = f"Temperatura promedio en {location} {_temperature} grados centigrados, estado del clima {_detailed_status}"
        self.speaker.speech_it(message)
        # alive(self.modulename + 'Temperature')

