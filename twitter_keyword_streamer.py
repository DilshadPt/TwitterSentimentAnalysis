import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
from config import consumer_key
from config import consumer_secret
from config import access_token
from config import access_token_secret
import json
import thread
from main_analyzer import main_classifier
import time
import csv

c = csv.writer(open("keyword_streamer_output.csv", "wb"))
c.writerow(["Tweet", "Result"])

tweets_data = []

def tweet_data_sender( threadName, delay):
	count = 0
	flag = 'changed'
	previous_val = 0
	
	while 1:
		time.sleep(delay)
		length = len(tweets_data)
		if previous_val != (length-1): 
			flag = 'changed'
        
		if ((length > 0) and (flag == 'changed')):
			tweets_data[length-1]
			result = main_classifier(tweets_data[length-1])
			print tweets_data[length-1]+':  '+result
			c.writerow([tweets_data[length-1].encode("utf-8"), result.encode("utf-8")])
			previous_val = length-1
			flag = 'notchanged'

class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        tweets_data.append(tweet['text'])
        return True

    def on_error(self, status):
        print status

def thread_starter():
	try:
		thread.start_new_thread( tweet_data_sender, ("Thread-1", 2, ) )
	except:
		print "Error: unable to start thread"


def twitter_keyword_streamer():

	thread_starter()
    #This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
	stream.filter(track=['python', 'javascript', 'ruby'])

twitter_keyword_streamer()
