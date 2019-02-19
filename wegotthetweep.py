import urllib2
import urllib
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twittercredentials



def getTweets(hashtags) :
    print("getTweets called")
    auth = OAuthHandler(twittercredentials.CONSUMER_KEY, twittercredentials.CONSUMER_SECRET)
    auth.set_access_token(twittercredentials.ACCESS_TOKEN, twittercredentials.ACCESS_TOKEN_SECRET)
#    stream = Stream(auth, listener)
#    stream.filter(track=hashtags)

def analyzeTweets(tweets) :
    print("analyzeTweets called")

def storeResults(results) :
    print("storeResults called")



def datloop(hashtags) :
    while True :
        tweets = getTweets(hashtags)
        results = analyzeTweets(tweets)
        storeResults(results)
        time.sleep(1)

hashtags = ['blessed', 'puppy']
url = 'https://twitter.com/search.json?q=%23puppy'

response = urllib2.urlopen(url)
print response.read()
datloop(hashtags)
 
