#!/usr/bin/python

import tweepy
import ConfigParser

from tweepy import OAuthHandler
from core.voicesynthetizer import VoiceSynthetizer

city = {'CHIS': 'Chiapas',  'NL': 'Nuevo Leon',}

class TwitterC(object):

    def __init__(self, voicesynthetizer):

        self.configuration()
        self.authentication()

        self.voicesynthetizer = voicesynthetizer

    def configuration(self):
        self.configuration = ConfigParser.ConfigParser()
        self.configuration.read('configuration/twitter.config')
        self.consumer_key = self.configuration.get('twitter','consumer_key')
        self.consumer_secret = self.configuration.get('twitter','consumer_secret')
        self.access_token = self.configuration.get('twitter','access_token')
        self.access_token_secret = self.configuration.get('twitter','access_token_secret')

    def authentication(self):
        self.authenticate = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.authenticate.set_access_token(self.access_token, self.access_token_secret)
        self.twitterapi = tweepy.API(self.authenticate)

    def sismologicomx(self):
        print '[Cancun] Twitter | Welcome ' + self.twitterapi.me().name
        self.voicesynthetizer.speechit('Servicio Sismologico Nacional, Universidad Nacional Autonoma de Mexico')

        user = self.twitterapi.get_user('SismologicoMX')
        for status in tweepy.Cursor(self.twitterapi.user_timeline, id='SismologicoMX').items(2):
            # self.twitterapi.update_status(status.text)
            status.text = status.text.replace("Loc", "Localizacion")
            status.text = status.text.replace("CD", "Ciudad")
            status.text = status.text.replace("Lat", "Latitud")
            status.text = status.text.replace("Lon", "Longitud")
            status.text = status.text.replace("Pf", "Profundidad")
            self.voicesynthetizer.speechit(status.text)

if __name__ == '__main__':

    mytest = TwitterC("google")
    mytest.sismologicomx()
