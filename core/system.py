#!/usr/bin/python

import commands
import logging
import numpy
import math

class System(object):

    def __init__(self):
        pass

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
        logging.info('System Top')
        status, output = commands.getstatusoutput("top -b -n 1 | grep Cpu")
        processor_usage = output.split()[1]
        status, output = commands.getstatusoutput("top -b -n 1 | grep Mem")
        memory = output.split()
        memory_usage = self.file_size(int(memory[4]))
        status, output = commands.getstatusoutput("top -b -n 1 | grep Tasks")
        tasks_total = output.split()[1]
        tasks_running = output.split()[3]
        output = 'Processor ' + processor_usage + '%'
        output = output + ' Memory ' + memory_usage
        output = output + ' Tasks ' + tasks_total
	return output

    def uname(self):
        logging.info('System Uname')
        status, output = commands.getstatusoutput("uname -a")
        kernel = output.split()[2]
	return kernel

    def execute(self):
        top = self.top()
        uname = self.uname()
        uname = 'Linux Kernel ' + uname
	final = top + ' ' + uname
        logging.info(final)
	return final

# End of File
