#!/usr/bin/python

import subprocess
import time

from core.irlp import Irlp

class Voice(object):

    def __init__(self):
        self.filename = "/tmp/voice.wav"
        self.proc = None
        self.irlp = Irlp()

    def filenameset(self, name):
        self.filename = name

    def recordstart(self):
        args = ['arecord', '-t', 'wav', '-f', 'S16_LE', '-r', '48000', self.filename]
        proc = subprocess.Popen(args)
        print("PID:", proc.pid)
        return proc

    def recordstop(self, proc):
        proc.kill()

    def record(self):
        time.sleep(1)
        if self.irlp.exists():
            while self.irlp.cosenabled() == 256:
                pass
            while self.irlp.cosenabled() == 0:
                pass
        proc = self.recordstart()
        if self.irlp.exists():
            while self.irlp.cosenabled() == 256:
                pass
        else:
            time.sleep(5)
        self.recordstop(proc)

    def play(self):
        subprocess.run(["aplay", self.filename])

    def erase(self):
        subprocess.run(["rm", self.filename])

# End of File
