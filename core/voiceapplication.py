#!/usr/bin/python

import ConfigParser
import json
import wit

from core.irlp import Irlp

class VoiceApplication(object):

    def __init__(self):
        self.irlp = Irlp()
        conf = ConfigParser.ConfigParser()
        conf.read("configuration/services.config")
        self.witaccesstoken = conf.get("wit", "accesstoken")

    def command(self):
        wit.init()
        if self.irlp.exists():
            while self.irlp.cosenabled() is 256:
                pass
            while self.irlp.cosenabled() is 0:
                pass
        wit.voice_query_start(self.witaccesstoken)
        if self.irlp.exists():
            while self.irlp.cosenabled() is 256:
                pass
        else:
            time.sleep(5)
        response = wit.voice_query_stop()
        wit.close()
        return response

    def text(self):
        response = self.command()
        return json.loads(response)['outcomes'][0]['_text']

    def action(self):
        response = self.command()
        return json.loads(response)['outcomes'][0]['intent']
        
