from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="2qz0rhReA523XEUWZ0kA08kKy"
consumer_secret="Vnrpb4Jq6BtI33nM9h0FrH6dy2lXWvWZW0jd1kG3Zwj485SJJe"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="1061737515806265344-EYmpwKI5qeIJPiaZeXsqJ2PWB6bHA4"
access_token_secret="pvjGkDAHqgevXDb6OdfQmsyUN7Ev7d77Gk3wga7wYQPin"

class Handler(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = Handler()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['terrified'])

