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
import sys

c = csv.writer(open("keyword_streamer_output.csv", "wb"))
c.writerow(["Tweet", "Result", "Stress"])


tweets_data = []
result_array = []
stress_array = []

def stress_finder(array):
	n_count = 0;
	p_count = 0;
	for prop in array:
		if prop == 'negative':
			n_count = n_count + 1
		else:
			p_count = p_count + 1
	total = len(array)
	stress_perc = (n_count*100) / total
	return stress_perc

def tweet_data_sender( threadName, delay):
	count = 0
	flag = 'changed'
	previous_val = 0
	check = 'notdone'
	min_stress = 'null'
	max_stress = 'null'
	avg_stress = 0
    
	while (check == 'notdone'):
		time.sleep(delay)
		length = len(tweets_data)
		if previous_val != (length-1): 
			flag = 'changed'
        
		if ((length > 0) and (flag == 'changed')):
			tweets_data[length-1]
			result = main_classifier(tweets_data[length-1])
			print tweets_data[length-1]+':  '+result
			result_array.append(result)
			
			previous_val = length-1
			flag = 'notchanged'
			stress = stress_finder(result_array)
			if ((min_stress == 'null') and (max_stress == 'null')):
				min_stress = stress
				max_stress = stress
			if (stress < min_stress):
				min_stress = stress
			if (stress > max_stress):
				max_stress = stress

			stress_array.append(stress)

			print 'Stress Percentage  '+str(stress)+'%'
			c.writerow([tweets_data[length-1].encode("utf-8"), result.encode("utf-8"), stress])

		if (length > 10):
			check = 'done'

	print 'out of the box'

	if stress < 16:
		level = 'no-stress'
	if stress > 16 and stress < 32:
		level = 'very weak'
	if stress > 32 and stress < 48:
		level =  'weak'
	if stress > 48 and stress < 64:
		level = 'moderate'
	if stress > 64 and stress < 80:
		level = 'severe'
	if stress > 80:
		level = 'very severe'

	print 'Stress level = '+level
	print "min_stress"+str(min_stress)
	print "max_stress"+str(max_stress)
	

	avg_stress = sum(stress_array)/len(stress_array)
	print sum(stress_array)
	print len(stress_array)
	print "Average"+str(avg_stress)
	c.writerow(["Minimum Stress", "Maximum Stress", "Average"])
	c.writerow([min_stress, max_stress, avg_stress])


class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        append_text = tweet['text'].replace(";", "")  # to avoid semi colon breaking csv, replaces semicolon with null
        tweets_data.append(append_text)
        return True

    def on_error(self, status):
        print status

def thread_starter():
	try:
		thread.start_new_thread( tweet_data_sender, ("Thread-1", 0.25, ) )
	except:
		print "Error: unable to start thread"


def twitter_keyword_streamer():

	thread_starter()
    #This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
	print "here in"
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
	# stream.filter(track=['python', 'javascript', 'ruby'])
	stream.filter(follow=['18839785', '136742287', '2903430392'])
	print "here"


twitter_keyword_streamer()
