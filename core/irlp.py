#!/usr/bin/python

import configparser
import subprocess
import logging
import os
import time


class Irlp(object):

    def __init__(self):
        logging.info('[Irlp]')
        self.conf = configparser.ConfigParser()
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
        result = subprocess.run(self.cosstate)
        return result.returncode

    def busy(self):
        logging.info('[Irlp] Busy')

        status = subprocess.run(self.cosstate).returncode
        while status == 256:
            subprocess.run(self.coscheck)
            time.sleep(int(self.irlpcostimer))
            status = subprocess.run(self.cosstate).returncode

    def idle(self):
        logging.info('[Irlp] Idle')
        self.busy()
        subprocess.run(self.off)

    def forceptt(self):
        logging.info('[Irlp] Force PTT')
        subprocess.run(self.forcekey)
        time.sleep(1)

    def forceunptt(self):
        logging.info('[Irlp] Force UnPTT')
        subprocess.run(self.forceunkey)

# End of File
