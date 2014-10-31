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

#TODO add input checks for 'count' option
def getOptions(include_rts_option=None, options_specified=None):
    if options_specified != None:
        print len(options_specified)
    default_options = {'count': 20,
                       'exclude_replies': True}
    if include_rts_option == True:
        default_options['include_rts'] = True
    selected_options = None
    use_defaults=raw_input("Would you like to use the default options? (With RTs, 20 tweets, no replies) Y/N\n")
    if use_defaults.lower() == "y":
        selected_options = default_options
    else:
        options = {}
        if include_rts_option == True:
            options['include_rts'] = True if raw_input("Include retweets (RTs)? Y/N\n").lower() == "y" else False
        options['count'] = int(raw_input("Number of tweets to show?\n"))
        options['exclude_replies'] = True if raw_input('Exclude replies? Y/N\n').lower() == "y" else False
        selected_options = options
    return selected_options

def printTweets(data):
    print "Printing tweets.."
    for i, tweet in enumerate(data, 1):
        handle=tweet["user"]["screen_name"]
        text=tweet["text"]
        print(u'{0}. {1} - {2}'.format(i, handle, text))
    print "\n Done printing tweets."

def viewMyTweets(session):
    selected_options = getOptions(include_rts_option=True, options_specified={"a":1, "b":4})
    data = getJSONData(session,"statuses/user_timeline.json",selected_options)
    printTweets(data)

def viewMyTimeline(session):
    selected_options = getOptions(include_rts_option=True)
    data = getJSONData(session, "statuses/home_timeline.json", selected_options)
    printTweets(data)

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
pin = raw_input('Enter PIN from browser: ')

session = twitter.get_auth_session(request_token,
    request_token_secret,
    method='POST',
    data={'oauth_verifier': pin})

print "Done getting Twitter session."

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
        print "Thanks for using UdiTwitClient!"
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


