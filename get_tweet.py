from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sent_mod as s
import json

#consumer key, consumer secret, access token, access secret.
ckey="OIKCszkBhnEFfb23n4CDNyM9Q"
csecret="ZmqXnvesSBVtOJtpy9SymtiJX0ejYjMCTN1cohjrMiEIj4tNx9"
atoken="754575162696015872-OiByOkiFnRD3wZRYYIqdVZLgSdPFD1A"
asecret="0uCtVHGQpQzAOSs61Lp3ZdSZKKr3m9HFhGgKJbCn5nQUm"


class listener(StreamListener):

    def on_data(self, data):
        #print(data)
        all_data = json.loads(data)
        tweet = all_data['text']
        sentiment_value = s.sentiment(tweet)
        print(tweet , sentiment_value)
        output = open("twitter_out.txt" , 'a')
        output.write(sentiment_value)
        output.write("\n")
        output.close()
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["modi"])
