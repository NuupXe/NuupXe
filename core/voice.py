#!/usr/bin/python

import commands
import subprocess
import time

from core.irlp import Irlp

class Voice(object):

    def __init__(self):
        self.filename = "voice.wav"
        self.proc = None

        self.irlp = Irlp()

    def filename(self, filename):
        self.filename = filename

    def recordstart(self):
        args = ['arecord','-t', 'wav', '-f', 'S16_LE', '-r', '48000', self.filename]
        proc = subprocess.Popen(args)
        print "PID:", proc.pid
        return proc

    def recordstop(self, proc):
        proc.kill()

    def play(self):
        status, output = commands.getstatusoutput("aplay " + self.filename)

    def erase(self):
        status, output = commands.getstatusoutput("rm " + self.filename)

if __name__ == '__main__':

    mytest = Voice()
    mytest.record()
    mytest.play()
    mytest.erase()

