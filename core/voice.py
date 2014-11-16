#!/usr/bin/python

import commands
import subprocess
import time

class Voice(object):

    def __init__(self):
        self.filename = "voice.wav"
        self.proc = None

    def record_filename(self, name):
        self.filename = name

    def record_start(self):
        args = ['arecord','-t', 'wav', '-f', 'S16_LE', '-r', '48000', self.filename]
        proc = subprocess.Popen(args)
        print "PID:", proc.pid
        return proc

    def record_stop(self, proc):
        proc.kill()

    def play(self):
        status, output = commands.getstatusoutput("aplay " + self.filename)

    def erase(self):
        status, output = commands.getstatusoutput("rm " + self.filename)

if __name__ == '__main__':

    mytest = Voice()

