import ConfigParser
import time
import sys
from socket import *

class AprsNet(object):

    def __init__(self):

        self.configuration()

    def configuration(self):
        self.conf = ConfigParser.ConfigParser()
        self.services = "configuration/services.config"
        self.conf.read(self.services)
        self.server = self.conf.get("aprsnet", "server")
        self.port = self.conf.get("aprsnet", "port")
        self.user = self.conf.get("aprsnet", "user")
        self.password = self.conf.get("aprsnet", "password")
        self.address = self.conf.get("aprsnet", "address")
        self.path = self.conf.get("aprsnet", "path")
        self.position = self.conf.get("aprsnet", "position")
        self.position_set(self.position)

    def server_open(self):
        self.socketid = socket(AF_INET, SOCK_STREAM)
        self.socketid.connect((self.server, int(self.port)))
        self.socketid.send('user ' + self.user + ' pass ' + self.password + ' vers "Experimental Project" \n')

    def server_close(self):
        self.socketid.shutdown(0)
        self.socketid.close()

    def address_set(self, address):
        self.address = address

    def position_set(self, position):
        self.position = '=' + position + '-'

    def send_message(self, message):
        self.server_open()
        self.socketid.send(self.address + self.path + self.position + message +'\n')
        print("packet sent: " + time.ctime() )
        self.server_close()

    def send_packet(self, packet):
        self.server_open()
        self.socketid.send(packet +'\n')
        print("packet sent: " + time.ctime() )
        self.server_close()
