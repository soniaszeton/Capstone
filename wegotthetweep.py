import time



def getTweets(hashtags) :
    print("getTweets called")

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

datloop(hashtags)
 
