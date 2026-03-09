#!/usr/bin/python

import logging
import time

DAYS = {
    'Monday': 'Lunes',      'Tuesday': 'Martes',    'Wednesday': 'Miercoles',
    'Thursday': 'Jueves',   'Friday': 'Viernes',    'Saturday': 'Sabado',
    'Sunday': 'Domingo',
}

MONTHS = {
    'January': 'Enero',     'February': 'Febrero',  'March': 'Marzo',
    'April': 'Abril',       'May': 'Mayo',           'June': 'Junio',
    'July': 'Julio',        'August': 'Agosto',      'September': 'Septiembre',
    'October': 'Octubre',   'November': 'Noviembre', 'December': 'Diciembre',
}


class Clock(object):

    def __init__(self, voicesynthesizer):
        self.modulename = 'Clock'
        self.voicesynthesizer = voicesynthesizer

    def date(self):
        logging.info(self.modulename + ' Date')
        day_name = DAYS[time.strftime("%A")]
        day_num = time.strftime("%d").lstrip('0')
        month_name = MONTHS[time.strftime("%B")]
        year = time.strftime("%Y")
        text = f"{day_name} {day_num} de {month_name} de {year}"
        self.voicesynthesizer.speech_it(text)

    def hour(self):
        logging.info(self.modulename + ' Hour')
        h = int(time.strftime("%H"))
        m = int(time.strftime("%M"))
        prefix = "Es la" if h == 1 else "Son las"
        hour_word = "hora" if h == 1 else "horas"
        if m == 0:
            text = f"{prefix} {h} {hour_word} en punto"
        elif m == 1:
            text = f"{prefix} {h} {hour_word} y 1 minuto"
        else:
            text = f"{prefix} {h} {hour_word} y {m} minutos"
        self.voicesynthesizer.speech_it(text)

# End of File
