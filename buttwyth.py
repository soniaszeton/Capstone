from twython import Twython
import twittercredentials
import json
import time
import boto3
import sys

userKeyword = sys.argv[1]

twitter = Twython(twittercredentials.CONSUMER_KEY, twittercredentials.CONSUMER_SECRET, twittercredentials.ACCESS_TOKEN, twittercredentials.ACCESS_TOKEN_SECRET)

s3 = boto3.resource('s3')

#results = twitter.cursor(twitter.search, q='wholesome', count=1, lang='en')
#results = twitter.cursor(twitter.search, q='puppy', count=1, lang='en', since_id=1097719009808662529)
def getInitialID(keyword):
    firstTweet = 0
    first_result = twitter.search(count=1, q=keyword)
    try:
        for tweet in first_result['statuses']:
            firstTweet = tweet['id']
            print 'Tweet ID: ', firstTweet 
    except TwythonError as e:
        print(e)
    return firstTweet

def getTweets(keyword, tweetID):
    counter = 0
    results = twitter.search(q=keyword, lang='en', since_id=tweetID)
    try:
        for result in results['statuses']:
            tweet_text = result['text']
            print 'Tweet Text: ', tweet_text
            counter += 1
    except TwythonError as e:
        print(e)
    return counter


#wholesomecount = 0

#for result in results:
#    filtered = dict((key, value) for key, value in result.iteritems() if key == "text")
#
#    print(json.dumps(filtered, indent=4, sort_keys=True))
#    wholesomecount += 1
#    
#
#print(wholesomecount)


#IF 1 tweet = 1 call, maybe eliminate RT to cut back?


currentcount = 0
#wordID = getInitialID('excited')

while True:
    wordID = 0
    while(wordID == 0):
        time.sleep(1)
        wordID = getInitialID(userKeyword)
    time.sleep(4)
    currentcount = getTweets(userKeyword, wordID)
    print 'Excited Count: ', currentcount

    #write to file in s3 bucket
    s3.Bucket('szeton-capstone').put_object(Key='tweetcounter.txt', Body=str(currentcount))


    #maybe need to update the tweet ID so no repeats? Unsure.
