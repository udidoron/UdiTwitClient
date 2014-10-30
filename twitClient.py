#!/usr/bin/env python

import argparse
import threading
import os
from rauth import OAuth1Service

parser = argparse.ArgumentParser() #TODO add argument parsing
toQuit = False

print os.getenv("twit_client_consumer_key", "NOPE!")
print os.getenv("twit_client_consumer_secret", "GUESS AGAIN!")
print os.getenv("twat_client", "This one isn't supposed to work")

#Getting Twitter session
"""
twitter = OAuth1Service(
    name='twitter',
    consumer_key='J8MoJG4bQ9gcmGh8H7XhMg',
    consumer_secret='7WAscbSy65GmiVOvMU5EBYn5z80fhQkcFWSLMJJu4',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    base_url='https://api.twitter.com/1.1/')
"""