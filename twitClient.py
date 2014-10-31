#!/usr/bin/env python

import argparse
import threading
import os
from rauth import OAuth1Service

#parser = argparse.ArgumentParser() #TODO add argument parsing
toQuit = False

def getJSONData(session, url, options):
    data = session.get(url, params=options)
    return data.json()

def viewMyTweets(session):
    default_options = {'include_rts': True,
                       'count': 20,
                       'exclude_replies': True}
    use_defaults=raw_input("Would you like to use the default options? (With RTs, 20 tweets, no replies) Y/N\n")
    if use_defaults.lower() == "y":
        data = getJSONData(session,"statuses/user_timeline.json",default_options)
        print "Printing tweets.."
        for i, tweet in enumerate(data, 1):
            handle=tweet["user"]["screen_name"]
            text=tweet["text"]
            print(u'{0}. {1} - {2}'.format(i, handle, text))
    else:
        print "Sorry, not yet implemented"

def viewMyTimeline(session):
    print "Sorry, not implemented yet :("

def viewMyDms(session):
    print "No DMs for you! Come back - one year!"

#Type = "mytweets"/"tweets"/"dms"
def viewRecent(type, session):
    if type == "mytweets":
        viewMyTweets(session)
    elif type == "tweets":
        viewMyTimeline(session)
    elif type == "dms":
        viewMyDms(session)

def tweet(session):
    print "Maybe in a later version."


#Getting Twitter session
print "Getting Twitter session.."
twitter = OAuth1Service(
    name='twitter',
    consumer_key=os.getenv("twit_client_consumer_key", "NOPE!"),
    consumer_secret=os.getenv("twit_client_consumer_secret", "GUESS AGAIN!"),
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    base_url='https://api.twitter.com/1.1/')

request_token, request_token_secret = twitter.get_request_token()
authorize_url = twitter.get_authorize_url(request_token)

print('Visit this URL in your browser: {url}'.format(url=authorize_url))
pin = read_input('Enter PIN from browser: ')

session = twitter.get_auth_session(request_token,
    request_token_secret,
    method='POST',
    data={'oauth_verifier': pin})

print "Done getting Twitter sessions."

while toQuit == False:
    print "What would you like to do?"
    print "Choose 1 for viewing last tweets on your timeline,"
    print "2 for viewing your last tweets,"
    print "3 for viewing your last DMs,"
    print "4 for tweeting something,"
    print "q to quit"
    choice = raw_input("Enter choice\n")
    if choice.lower() == "q": #wish Python had switch-case..
        toQuit=True
    elif choice == "1":
        viewRecent("tweets", session)
    elif choice == "2":
        viewRecent("mytweets", session)
    elif choice == "3":
        viewRecent("dms", session)
    elif choice == "4":
        tweet(session)
    else:
        print "Invalid choice."


