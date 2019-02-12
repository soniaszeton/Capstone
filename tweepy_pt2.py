from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twittercredentials

# # # # Twitter Authenticator # # # #
class TwitterAuthenticator():

  def authenticate_twitter_app(self):
    auth = OAuthHandler(twittercredentials.CONSUMER_KEY, twittercredentials.CONSUMER_SECRET)
    auth.set_access_token(twittercredentials.ACCESS_TOKEN, twittercredentials.ACCESS_TOKEN_SECRET)
    return auth

class TwitterStreamer():

  #Class for streaming and processing live tweets

  #fetched_tweets_filename is where the tweets are being sent to instead of just the terminal
  #handles Twitter authentification and the connection to the Twitter Streaming API
  def __init__(self):
    self.twitter_authenticator = TwitterAuthenticator()

  def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
    listener = TwitterListener(fetched_tweets_filename)

    auth = self.twitter_authenticator.authenticate_twitter_app()

    stream = Stream(auth, listener)

    stream.filter(track=hash_tag_list)
    

class TwitterListener(StreamListener):

  #This is a basic listener class that just prints received tweets to stdout

  def init (self, fetched_tweets_filename):
    self.fetched_tweets_filename = fetched_tweets_filename

  def on_data(self, data):
    try:
      print(data)
      with open(self.fetched_tweets_filename, 'a') as tf:
        tf.write(data)
      return True
    except BaseException as e:
      print("Error on_data: %s" % str(e))
    return True

  def on_error(self, status):
    #Return false if rate limit occurs to avoid getting kicked out
    if status == 420:
      return False
    print(status)


if __name__=="__main__":
  #listener = StdOutListener()
  #auth = OAuthHandler(twittercredentials.CONSUMER_KEY, twittercredentials.CONSUMER_SECRET)
  #auth.set_access_token(twittercredentials.ACCESS_TOKEN, twittercredentials.ACCESS_TOKEN_SECRET)

  #stream = Stream(auth, listener)

  #stream.filter(track=['happy', 'blessed', 'puppy'])

  mylist = ["happy", "blessed", "engaged", "puppy", "wholesome"]
  fetchedfilename = "tweets.json"

  twitterstreamer = TwitterStreamer()
  twitterstreamer.stream_tweets(fetchedfilename, mylist)
