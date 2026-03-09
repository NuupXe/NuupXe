#!/usr/bin/python

import subprocess
import logging
import psutil

from core.utilities import BytesToHuman

class System(object):

    def __init__(self):
        pass

    def cpu(self):
        output = psutil.cpu_times_percent(interval=1, percpu=False)
        return "%.1f" % output.system

    def memory(self):
        output = psutil.virtual_memory()
        return BytesToHuman(output.total)

    def kernelVersion(self):
        logging.info('System Uname')
        result = subprocess.run(["uname", "-a"], capture_output=True, text=True)
        return result.stdout.split()[2] if result.stdout else None

# End of File
