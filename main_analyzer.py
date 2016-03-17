import nltk
from negativetweets import neg_tweets
from positivetweets import pos_tweets

# def train(labeled_featuresets, estimator=ELEProbDist):
#     ...
#     # Create the P(label) distribution
#     label_probdist = estimator(label_freqdist)
#     ...
#     # Create the P(fval|label, fname) distribution
#     feature_probdist = {}
#     ...
#     return NaiveBayesClassifier(label_probdist, feature_probdist)

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in document_words:
        features['contains(%s)' % word] = (word in document_words)
    return features

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features



#print tweets

def main_classifier(tweettotest):
    tweets = []
    for (words, sentiment) in pos_tweets + neg_tweets:
        words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
        tweets.append((words_filtered, sentiment))

    word_features = get_word_features(get_words_in_tweets(tweets))
    #print word_features
    training_set = nltk.classify.apply_features(extract_features, tweets)
    # print training_set
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    # print classifier
    # tweettotest = 'I dilshad tired this sunday'
    return classifier.classify(extract_features(tweettotest.split()))