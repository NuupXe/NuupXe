#!/usr/bin/python

import tweepy
import ConfigParser

from tweepy import OAuthHandler

class TwitterC(object):

    def __init__(self):

        self.configuration()
        self.authentication()

    def configuration(self):
        self.configuration = ConfigParser.ConfigParser()
        self.configuration.read('configuration/services.config')
        self.consumer_key = self.configuration.get('twitter','consumer_key')
        self.consumer_secret = self.configuration.get('twitter','consumer_secret')
        self.access_token = self.configuration.get('twitter','access_token')
        self.access_token_secret = self.configuration.get('twitter','access_token_secret')

    def authentication(self):
        self.authenticate = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.authenticate.set_access_token(self.access_token, self.access_token_secret)
        self.twitterapi = tweepy.API(self.authenticate)

    def timeline_get(self, user, items):
	try:
            self.twitterapi.get_user(user)
	    return tweepy.Cursor(self.twitterapi.user_timeline, id=user).items(items)
	except:
	    print '[Cancun] Twitter | Timeline Get Error ...'

    def timeline_set(self, status):
        try:
	    self.twitterapi.update_status(status)
        except:
            print '[Cancun] Twitter | Timeline Set Error'
