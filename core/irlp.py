#!/usr/bin/python

import ConfigParser
import commands
import os
import time


class Irlp(object):

    def __init__(self):
        logging.info('[Irlp]')
        self.conf = ConfigParser.ConfigParser()
        self.filepath = "configuration/general.config"
        self.conf.read(self.filepath)
        self.irlppath = self.conf.get("irlp", "path")
        self.irlpcostimer = self.conf.get("irlp", "costimer")

        self.coscheck = self.irlppath + 'bin/coscheck'
        self.cosstate = self.irlppath + 'bin/cosstate'
        self.pttstate = self.irlppath + 'bin/pttstate'
        self.off = self.irlppath + 'scripts/off'
        self.forcekey = self.irlppath + 'bin/forcekey'
        self.forceunkey = self.irlppath + 'bin/forceunkey'
        self.activeflag = self.irlppath + 'local/active'

    def exists(self):
        logging.info('[Irlp] Exists')
        return os.path.isfile(self.irlppath + 'bin/coscheck')

    def active(self):
        logging.info('[Irlp] Active')
        return os.path.isfile(self.activeflag)

    def cosenabled(self):
        logging.info('[Irlp] CosEnabled')
        status, output = commands.getstatusoutput(self.cosstate)
        return status

    def busy(self):
        logging.info('[Irlp] Busy')
        status, output = commands.getstatusoutput(self.cosstate)
        while status is 256:
            status, output = commands.getstatusoutput(self.coscheck)
            time.sleep(int(self.irlpcostimer))
            status, output = commands.getstatusoutput(self.cosstate)

    def idle(self):
        logging.info('[Irlp] Idle')
        self.busy()
        commands.getstatusoutput(self.off)

    def forceptt(self):
        logging.info('[Irlp] Force PTT')
        commands.getstatusoutput(self.forcekey)
        time.sleep(1)

    def forceunptt(self):
        logging.info('[Irlp] Force UnPTT')
        commands.getstatusoutput(self.forceunkey)

# End of File
