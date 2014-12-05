#!/usr/bin/python

import ConfigParser
import commands

from core.aprsnet import AprsNet
from core.phonetic import Phonetic
from core.voicesynthetizer import VoiceSynthetizer

class CommandTerminal(object):

    def __init__(self, voicesynthetizer):

        self.aprs = AprsNet()
        self.phonetic = Phonetic()
        self.voicesynthetizer = voicesynthetizer

    def topcpu(self):
        print '[Cancun] Command Top Cpu Info'
        callsign = 'XE1GYQ-1'

        self.aprs.address_set(callsign)
        self.aprs.position_set('=2036.96N/10324.46W-')

        status, output = commands.getstatusoutput("top -b -n 1 | grep Cpu")
        self.aprs.send_packet(output)
        data = ' '.join(self.phonetic.decode('aprs.fi/')) + ' '.join(self.phonetic.decode(callsign))
        self.voicesynthetizer.speechit("Datos de Uso de nuestro Procesador en la direccion " + data)
        
    def topmem(self):
        print '[Cancun] Command Top Mem Info'
        callsign = 'XE1GYQ-2'

        self.aprs.address_set(callsign)
        self.aprs.position_set('=2036.96N/10324.34W-')

        status, output = commands.getstatusoutput("top -b -n 1 | grep Mem")
        self.aprs.send_packet(output)
        data = ' '.join(self.phonetic.decode('aprs.fi/')) + ' '.join(self.phonetic.decode(callsign))
        self.voicesynthetizer.speechit("Datos de Uso de nuestra Memoria en la direccion " + data)

    def toptasks(self):
        print '[Cancun] Command Top Tasks Info'
        callsign = 'XE1GYQ-1'

        self.aprs.address_set(callsign)
        self.aprs.position_set('=2036.96N/10324.46W-')

        status, output = commands.getstatusoutput("top -b -n 1 | grep Tasks")
        self.aprs.send_packet(output)
        data = ' '.join(self.phonetic.decode('aprs.fi/')) + ' '.join(self.phonetic.decode(callsign))
        self.voicesynthetizer.speechit("Datos de Uso de Tareas en la direccion " + data)

    def toptasks(self):
        print '[Cancun] Command Uname Info'
        callsign = 'XE1GYQ-2'

        self.aprs.address_set(callsign)
        self.aprs.position_set('=2036.96N/10324.34W-')

        status, output = commands.getstatusoutput("uname -a")
        self.aprs.send_packet(output)
        data = ' '.join(self.phonetic.decode('aprs.fi/')) + ' '.join(self.phonetic.decode(callsign))
        self.voicesynthetizer.speechit("Datos de Version del Kernel en la direccion " + data)

    def execute(self):
        # self.topcpu()
        # self.topmem()
        self.toptasks()
        self.uname()

if __name__ == '__main__':

    mytest = CommandTerminal()
