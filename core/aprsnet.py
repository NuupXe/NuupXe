import configparser
import logging
from socket import *

class AprsNet:

    def __init__(self):
        self.configuration()

    def configuration(self):
        self.conf = configparser.ConfigParser()
        self.services = "configuration/services.config"
        self.conf.read(self.services)
        self.server = self.conf.get("aprsnet", "server")
        self.port = int(self.conf.get("aprsnet", "port"))
        self.user = self.conf.get("aprsnet", "user")
        self.password = self.conf.get("aprsnet", "password")
        self.address = self.conf.get("aprsnet", "address")
        self.path = self.conf.get("aprsnet", "path")
        self.position = self.conf.get("aprsnet", "position")
        self.position_set(self.position)

    def server_open(self):
        self.socketid = socket(AF_INET, SOCK_STREAM)
        self.socketid.connect((self.server, self.port))
        message = f'user {self.user} pass {self.password} vers "Experimental Project"'.encode()
        self.socketid.send(message)

    def server_close(self):
        self.socketid.shutdown(SHUT_RDWR)
        self.socketid.close()

    def address_set(self, address):
        self.address = address.upper()

    def position_set(self, position):
        self.position = f'={position}-'

    def send_message(self, message):
        self.server_open()
        packet = f'{self.address}{self.path}{self.position}{message}\n'
        self.socketid.send(packet.encode())
        logging.info(packet)
        self.server_close()

    def send_packet(self, packet):
        self.server_open()
        packet = packet + '\n'
        self.socketid.send(packet.encode())
        logging.info(packet)
        self.server_close()
