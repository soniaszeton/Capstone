from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twittercredentials

class TwitterStreamer():

  #Class for streaming and processing live tweets

  #fetched_tweets_filename is where the tweets are being sent to instead of just the terminal
  #handles Twitter authentification and the connection to the Twitter Streaming API
  def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
    listener = StdOutListener()
    auth = OAuthHandler(twittercredentials.CONSUMER_KEY, twittercredentials.CONSUMER_SECRET)
    auth.set_access_token(twittercredentials.ACCESS_TOKEN, twittercredentials.ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)

    stream.filter(track=hash_tag_list)
    

class StdOutListener(StreamListener):

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
