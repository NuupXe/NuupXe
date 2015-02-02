#!/usr/bin/python

import ConfigParser
import commands
import numpy
import math

from core.aprsnet import AprsNet
from core.phonetic import Phonetic
from core.voicesynthetizer import VoiceSynthetizer

class CommandTerminal(object):

    def __init__(self, voicesynthetizer):

        self.aprs = AprsNet()
        self.phonetic = Phonetic()
        self.voicesynthetizer = voicesynthetizer

    def file_size(self, size):
        size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size,1024)))
        p = math.pow(1024,i)
        s = round(size/p,2)
        if (s > 0):
            return '%s %s' % (s,size_name[i])
        else:
            return '0B'

    def top(self):
        print '[Cancun] Command Top'
        callsign = 'XE1GYQ-1'

        self.aprs.address_set(callsign)
        self.aprs.position_set('2036.96N/10324.46W')

        status, output = commands.getstatusoutput("top -b -n 1 | grep Cpu")
        processor_usage = output.split()[1]
        self.voicesynthetizer.speechit(processor_usage + '% en uso de Procesador')
        status, output = commands.getstatusoutput("top -b -n 1 | grep Mem")
        memory = output.split()
        memory_usage = self.file_size(int(memory[4]))
        self.voicesynthetizer.speechit(memory_usage + ' en uso de Memoria')
        status, output = commands.getstatusoutput("top -b -n 1 | grep Tasks")
        tasks_total = output.split()[1]
        tasks_running = output.split()[3]
        self.voicesynthetizer.speechit(tasks_total + ' Tareas en total con ' + tasks_running + ' tareas corriendo')
        output = 'Processor ' + processor_usage + '%'
        output = output + ' Memory ' + memory_usage
        output = output + ' Tasks Total ' + tasks_total
        output = output + ' Tasks Running ' + tasks_running
        self.aprs.send_message(output)
        data = ' '.join(self.phonetic.decode('aprs.fi/')) + ' '.join(self.phonetic.decode(callsign))
        self.voicesynthetizer.speechit("Datos del procesador, memoria y tareas del sistema en la direccion " + data)

    def uname(self):
        print '[Cancun] Command Uname'
        callsign = 'XE1GYQ-2'

        self.aprs.address_set(callsign)
        self.aprs.position_set('2036.96N/10324.34W')

        status, output = commands.getstatusoutput("uname -a")
        self.aprs.send_message(output)
        data = ' '.join(self.phonetic.decode('aprs.fi/')) + ' '.join(self.phonetic.decode(callsign))
        self.voicesynthetizer.speechit("Datos de Version del Kernel en la direccion " + data)

    def execute(self):
        self.top()
        self.uname()

if __name__ == '__main__':

    mytest = CommandTerminal()
