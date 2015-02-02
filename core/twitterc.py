#!/usr/bin/python

import tweepy
import twython
import ConfigParser
from twython import Twython

from tweepy import OAuthHandler
from twython import Twython

class TwitterC(object):

    def __init__(self, agent):

        self.agent = agent
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
        if self.agent == 'tweepy':
            self.authenticate = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            self.authenticate.set_access_token(self.access_token, self.access_token_secret)
            self.twitter = tweepy.API(self.authenticate)
        elif self.agent == 'twython':
            self.twitter = Twython(self.consumer_key,self.consumer_secret,self.access_token,self.access_token_secret)

    def timeline_get(self, user, items):
	try:
            if self.agent == 'tweepy':
                self.twitter.get_user(user)
                return tweepy.Cursor(self.twitterapi.user_timeline, id=user).items(items)
            elif self.agent == 'twython':
                return self.twitter.get_user_timeline(screen_name=user, include_rts=True, count=items)
	except:
	    print '[Cancun] Twitter | Timeline Get Error ...'

    def timeline_set(self, status, media):
        if self.agent == 'tweepy':
            self.twitter.update_status(status)
        elif self.agent == 'twython':
            if media:
                photo = open(media,'rb')
                self.twitter.update_status_with_media(media=photo, status=status)
            else:
                self.twitter.update_status(status=status)
