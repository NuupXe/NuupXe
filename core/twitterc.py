#!/usr/bin/python

import logging
import configparser

from twython import Twython

class TwitterC(logging.Handler):

    def __init__(self, agent):

        logging.Handler.__init__(self)
        self.agent = agent
        self.configuration()
        self.authentication()

    def configuration(self):
        logging.info('[NuupXe] Twitter Configuration')
        self.conf = configparser.ConfigParser()
        self.conf.read('configuration/services.config')
        self.consumer_key = self.conf.get('twitter', 'consumer_key')
        self.consumer_secret = self.conf.get('twitter', 'consumer_secret')
        self.access_token = self.conf.get('twitter', 'access_token')
        self.access_token_secret = self.conf.get('twitter', 'access_token_secret')

    def authentication(self):
        logging.info('[NuupXe] Twitter Authentication')
        self.twitter = Twython(self.consumer_key, self.consumer_secret,
                               self.access_token, self.access_token_secret)

    def timeline_get(self, user, items):
        logging.info('[NuupXe] Twitter TimelineGet')
        try:
            return self.twitter.get_user_timeline(screen_name=user, include_rts=True, count=items)
        except Exception:
            logging.info('[NuupXe] Twitter | Timeline Get Error ...')

    def timeline_set(self, status, media):
        logging.info('[NuupXe] Twitter TimelineSet')
        if media:
            photo = open(media, 'rb')
            self.twitter.update_status_with_media(media=photo, status=status)
        else:
            self.twitter.update_status(status=status)

# End of File
