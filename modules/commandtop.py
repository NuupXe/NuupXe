#!/usr/bin/python

import ConfigParser
import commands

from core.aprsnet import AprsNet
from core.phonetic import Phonetic
from core.voicesynthetizer import VoiceSynthetizer

class CommandTop(object):

    def __init__(self, voicesynthetizer):

        self.aprs = AprsNet()
        self.phonetic = Phonetic()
        self.voicesynthetizer = voicesynthetizer

    def cpu(self):
        print '[Cancun] Command Top Cpu Info'
        callsign = 'XE1GYQ-1'

        self.aprs.address_set(callsign)
        self.aprs.position_set('=2036.96N/10324.46W-')

        status, output = commands.getstatusoutput("top -b -n 1 | grep Cpu")
        self.aprs.send_packet(output)
        data = ' '.join(self.phonetic.decode('aprs.fi/')) + ' '.join(self.phonetic.decode(callsign))
        self.voicesynthetizer.speechit("Datos de Uso de nuestro Procesador en la direccion " + data)
        
    def mem(self):
        print '[Cancun] Command Top Mem Info'
        callsign = 'XE1GYQ-2'

        self.aprs.address_set(callsign)
        self.aprs.position_set('=2036.96N/10324.34W-')

        status, output = commands.getstatusoutput("top -b -n 1 | grep Mem")
        self.aprs.send_packet(output)
        data = ' '.join(self.phonetic.decode('aprs.fi/')) + ' '.join(self.phonetic.decode(callsign))
        self.voicesynthetizer.speechit("Datos de Uso de nuestra Memoria en la direccion " + data)

    def tasks(self):
        print '[Cancun] Command Top Tasks Info'
        callsign = 'XE1GYQ-3'

        self.aprs.address_set(callsign)
        self.aprs.position_set('=2036.96N/10324.58W-')

        status, output = commands.getstatusoutput("top -b -n 1 | grep Tasks")
        self.aprs.send_packet(output)
        data = ' '.join(self.phonetic.decode('aprs.fi/')) + ' '.join(self.phonetic.decode(callsign))
        self.voicesynthetizer.speechit("Datos de Uso de Tareas en la direccion " + data)

    def execute(self):
        self.cpu()
        self.mem()
        self.tasks()

if __name__ == '__main__':

    mytest = CommandTop()
