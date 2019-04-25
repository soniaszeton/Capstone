# -*- coding: iso-8859-15 -*-

from __future__ import absolute_import, print_function
import time
import twittercredentials

# import the twitter streaming API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# import the AWS S3 API
import boto3
s3 = boto3.resource('s3')

# a mapping of LED color to emotions
emotions = {
    'red': 'anger',
    'orange': 'fear',
    'yellow': 'happiness',
    'green': 'environmental',
    'cyan': 'tranquility',
    'blue': 'sadness',
    'violet': 'love'
}

# the list of keywords for each type of emotion
wordLists = [
    ['hate', 'pissed', 'mad'],
    ['scared', 'afraid', 'terrified'],
    ['puppy', 'happy', 'excited'],
    ['green', 'reduce', 'earth'],
    ['hope', 'thankful', 'relax'],
    ['sad', 'lonely', 'upset'],
    ['love', 'proud', 'married']
]

# the flattened list of keywords to filter the tweets on
keywords = []
for sublist in wordLists:
    for item in sublist:
        keywords.append(item)

# twitter credentials
consumer_key=twittercredentials.CONSUMER_KEY
consumer_secret=twittercredentials.CONSUMER_SECRET
access_token=twittercredentials.ACCESS_TOKEN
access_token_secret=twittercredentials.ACCESS_TOKEN_SECRET

# the number of seconds since the last reset
checkpoint = int(round(time.time()))

# the initial values of the emotions
values = [0, 0, 0, 0, 0, 0, 0]

# define a handler class for when data is received
class Handler(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        process_data(data)
        return True

    def on_error(self, status):
        print(status)


def process_data(data):
    global checkpoint
    global values
    current = int(round(time.time()))
    if current > checkpoint + 10:
        # every 10 seconds write current values out to S3 and reset them
        checkpoint = current
        body = '\n'.join([str(i) for i in values])
        print("The current values are: ")
        print("anger: " + str(values[0]))
        print("fear: " + str(values[1]))
        print("happiness: " + str(values[2]))
        print("eco-friendly: " + str(values[3]))
        print("contentment: " + str(values[4]))
        print("sadness: " + str(values[5]))
        print("love: " + str(values[6]))
        print("")
        s3.Bucket('szeton-capstone').put_object(Key='tweetcounter.txt', Body=body)
        values = [0, 0, 0, 0, 0, 0, 0]
    string = str(data)
    index = 0
    for words in wordLists:
        for keyword in words:
            if keyword in string:
                values[index] += 1
        index += 1

# connect to the twitter streaming API
if __name__ == '__main__':
    handler = Handler()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, handler)
    stream.filter(track=keywords)

