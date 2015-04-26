#!/usr/bin/python

import logging
import time

from core.alive import alive
from core.voicesynthetizer import VoiceSynthetizer

days = {'Monday': 'Lunes',  'Tuesday': 'Martes',    'Wednesday': 'Miercoles',
    'Thursday': 'Jueves',   'Friday': 'Viernes',    'Saturday': 'Sabado',
    'Sunday': 'Domingo',
    }

months = {'January': 'Enero',   'February': 'Febrero',  'March': 'Marzo',
    'April': 'Abril',   'May': 'Mayo',      'June': 'Junio',
    'July': 'Julio',    'August': 'Agosto', 'September': 'Septiembre',
    'October': 'Octubre',   'November' : 'Noviembre',   'December': 'Diciembre'
    }

class Clock(object):

    def __init__(self, voicesynthetizer):
        self.modulename = 'Clock'
        self.voicesynthetizer = voicesynthetizer

    def date(self):
        logging.info(self.modulename + ' Date')
        date = days[time.strftime("%A")] + " "  + time.strftime("%d").lstrip('0')
        date = date + " de " + months[time.strftime("%B")] + " de " + time.strftime("%Y")
        self.voicesynthetizer.speechit(date)
        alive(modulename=self.modulename + 'Date', modulemessage=date)

    def hour(self):
        logging.info(self.modulename + ' Hour')
        hour = "Son las " + time.strftime("%H") + " horas y " + time.strftime("%M") + " minutos"
        self.voicesynthetizer.speechit(hour)
        alive(modulename=self.modulename + 'Hour', modulemessage=hour)

# End of File
