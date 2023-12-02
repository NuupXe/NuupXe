#!/usr/bin/python

import subprocess
import logging
import numpy
import math
import psutil

from core.utilities import BytesToHuman

class System(object):

    def __init__(self):
        pass

    def cpu(mode):
        output = psutil.cpu_times_percent(interval=1, percpu=False)
        return "%.1f" % output.system

    def memory(self):
        output = psutil.virtual_memory()
        return BytesToHuman(output.total)

    def kernelVersion(self):
        logging.info('System Uname')
        result = subprocess.run(["uname", "-a"])
        output = result.stdout
        error_output = result.stderr
        #print(f'{output error_output}')
        #return output.split()[2]
        return

# End of File
