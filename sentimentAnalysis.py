from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.sentiment import SentimentAnalyzer
from nltk.classify.util import accuracy
import csv
import os
def extractWords (sent):
    return dict([(word,True) for word in sent])

def cleanTweet (tweet):
    newtweetlist =[]
    wordlist = tweet.split()
    for word in wordlist:
        if word.isalnum():
            newtweetlist.append(word.lower())
        else :
            cleanword = "".join(c for c in word if c.isalpha())
            newtweetlist.append(cleanword.lower())

    return newtweetlist
def getTweets(dummy=False):
    filename = "Sentiment Analysis Dataset.csv"
    if not os.path.isfile(filename) or dummy:
        print ("WARNING : Not adding twitter dataset. Check readme")
        return ([],[])
    else :
        fp = open( filename, 'rb' )
        reader = csv.reader( fp, delimiter=',', quotechar='"', escapechar='\\' )
        tweetspos = []
        tweetsneg = []
        # skip the header
        next(reader)
        for row in reader:
            cleantw = cleanTweet(row[3])
            wordsT = extractWords(cleantw)
            if (int (row[1])==0 ): #negative tweet
                tweetsneg.append((wordsT,'neg'))
            elif (int(row[1])==1): # positive tweet
                tweetspos.append((wordsT,'pos'))
        if (len (tweetsneg)>0) :
            print ("Twitter data successfully added! ")
        return (tweetsneg,tweetspos)
def createClassifier (ignoreTweets=False):
    neg_ids = movie_reviews.fileids('neg')
    pos_ids = movie_reviews.fileids('pos')
    neg_sents = [(extractWords(movie_reviews.words(fileids=[f])),'neg') for f in neg_ids]
    pos_sents = [(extractWords(movie_reviews.words(fileids=[f])),'pos') for f in pos_ids]


    #if you dont want to process all tweets, just call :
    #getTweets(True)
    (neg_tweets,pos_tweets)  = getTweets(ignoreTweets)
    neg_sents = neg_sents+neg_tweets
    pos_sents = pos_sents + pos_tweets
    trainsizeneg = int (0.75*len(neg_sents))
    trainsizepos = int (0.75*len(pos_sents))


    all_train = neg_sents[:trainsizeneg] + pos_sents[:trainsizepos]
    all_test = neg_sents[trainsizeneg:] + pos_sents[trainsizepos:]
    # train size = 1500, test size = 500

    s_analyzer = SentimentAnalyzer()

    classifier = NaiveBayesClassifier.train (all_train)
    print accuracy(classifier,all_test)
    #classifier.show_most_informative_features()


    return classifier
    #return trainClassifier (training_set,test_set,s_analyzer)
def Classify (sentence,classifier):
    test_sentence = dict([(word,True) for word in sentence.split()])

    prob_dist = classifier.prob_classify(test_sentence)
    result = prob_dist.max()
    acc = prob_dist.prob(result)
    return (result,acc)

def DoAnalysis (sentence):
    classifier = createClassifier()
    return Classify(sentence,classifier)
if __name__=="__main__":
    print (DoAnalysis("I am happy"))
