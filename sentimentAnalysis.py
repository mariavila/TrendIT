from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.sentiment import SentimentAnalyzer
from nltk.classify.util import accuracy

def extractWords (sent):
    return dict([(word,True) for word in sent])
def createClassifier ():
    neg_ids = movie_reviews.fileids('neg')
    pos_ids = movie_reviews.fileids('pos')
    neg_sents = [(extractWords(movie_reviews.words(fileids=[f])),'neg') for f in neg_ids]
    pos_sents = [(extractWords(movie_reviews.words(fileids=[f])),'pos') for f in pos_ids]

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
def DoAnalysis (sentence):
    classifier = createClassifier()
    test_sentence = dict([(word,True) for word in sentence.split()])

    prob_dist = classifier.prob_classify(test_sentence)
    result = prob_dist.max()
    acc = prob_dist.prob(result)
    return (result,acc)
if __name__=="__main__":
    print (DoAnalysis("I am happy"))
