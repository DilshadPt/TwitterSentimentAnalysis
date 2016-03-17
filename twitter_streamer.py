import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from main_analyzer import main_classifier

consumer_key = 'FDlTtEIvmDP7mtRkDazVCDsos'
consumer_secret = 'uS0hFpvqj53fWia5PilSuG6Vht3JViGMXOgmJWDax023R09I77'
access_token = '136742287-krmFGhrFa9PlwiKPhUKeJ6KwchkAlhwiLgNoHK3M'
access_secret = 'hCC5h7ibvhflgFsPr5CcgU0mMaI2GUZz6MuX9lu8vIt3C'


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
count = 0
status_array = []
tweets_array = []

for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print str(count)+": "+status.text
    status_array.append(status.text)
    count = count + 1


count = 0    
for tweet in tweepy.Cursor(api.user_timeline).items():
    print str(count)+": "+tweet.text
    tweets_array.append(tweet.text)
    count = count + 1

# print status_array
# # print tweets_array
# test = 'I dilshad tired this sunday'
# result = main_classifier(test)
# print result
for prop in status_array:
	result = main_classifier(prop)
	print result