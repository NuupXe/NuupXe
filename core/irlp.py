#!/usr/bin/python

import ConfigParser
import commands
import time
import os

class Irlp(object):

    def __init__(self):

        self.conf = ConfigParser.ConfigParser()
        self.filepath = "configuration/general.config"
        self.conf.read(self.filepath)
        self.irlppath=self.conf.get("irlp", "path")
        self.irlpcostimer=self.conf.get("irlp", "costimer")

        self.coscheck=self.irlppath + 'bin/coscheck'
        self.cosstate=self.irlppath + 'bin/cosstate'
        self.off=self.irlppath + 'scripts/off'
        self.forcekey=self.irlppath + 'bin/forcekey'
        self.forceunkey=self.irlppath + 'bin/forceunkey'
        self.activeflag=self.irlppath + 'local/active'

    def active(self):
        return os.path.isfile(self.activeflag)

    def cosenabled(self):
        status, output = commands.getstatusoutput(self.cosstate)
        return status

    def busy(self):
        status, output = commands.getstatusoutput(self.cosstate)
        while status is 256:
            status, output = commands.getstatusoutput(self.coscheck)
            time.sleep(int(self.irlpcostimer))
            status, output = commands.getstatusoutput(self.cosstate)

    def idle(self):
        self.busy()
        commands.getstatusoutput(self.off)

    def forceptt(self):
        commands.getstatusoutput(self.forcekey)

    def forceunptt(self):
        commands.getstatusoutput(self.forceunkey)

if __name__ == '__main__':

    mytest = Irlp()
    mytest.cosenabled()
