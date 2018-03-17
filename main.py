import sys
sys.path.append("Reddit API")
import GetTop10
from sentimentAnalysis import createClassifier,Classify
from makeSubredditPredictions import SubredditProbability
def initReddit ():
    GetTop10.refresh_token()

def isclose(a,b):
    err = abs (a-b)
    if err<10:
        return True
    else:
         return False

def getOverallValues (classifier,posts):
    l = []
    for d in posts:
        print (d["title"])
        #print (Classify(d["title"],classifier))
        overall_pos = 0
        overall_neg = 0
        for com in d["comments"]:
            (res,acc) = Classify(com["body"],classifier)
            if (res=='pos'):
                overall_pos=overall_pos+(acc*com["upvotes"])
            else :
                overall_neg=overall_neg+(acc*com["upvotes"])

        percent_pos = 100*overall_pos/(overall_neg+overall_pos)
        percent_neg = 100*overall_neg/(overall_neg+overall_pos)
        value = 0
        if (isclose(percent_neg,percent_pos)):
            print ("     Neutral opinion")
        elif (percent_neg>percent_pos):
            print ("Negative opinion", percent_neg)
            value = -percent_neg
        else:
            print ("Positive opinion", percent_pos)
            value = percent_pos
        l.append((d["title"],value,d["sub"]))
    return l

def getSubredditNames (sub):
    l = []
    for elem in sub:
        l.append(elem["sub"])
    return l
def getTopSubredits (num=100,time="day"):
    subredits = GetTop10.get_top_posts_subreddits(num,time)
    subredNames= getSubredditNames(subredits)
    return subredits

def getDailyOutliers ():

    c = SubredditProbability()
    subreditsMonth = GetTop10.get_top_posts_subreddits(100,"month")
    subredNamesM = getSubredditNames(subreditsMonth)

    c.get_probabilities(subredNamesM)
    subreditsWeek = GetTop10.get_top_posts_subreddits(100,"week")
    subredNamesw = getSubredditNames(subreditsWeek)
    c.get_probabilities(subredNamesw)

    subreditsDay = GetTop10.get_top_posts_subreddits(100,"day")
    subredNamesDay = getSubredditNames(subreditsDay)
    print ("Daily outlier subredits:")
    outliers = []
    for subreddit in subredNamesDay:
        if c.is_outlier(subreddit):
            #print (subreddit)
            outliers.append(subreddit)
    print (len(outliers))
    return outliers
def getTopResults (n_posts=10, n_comments=50, timeperiod="day"):

    comments = GetTop10.get_top_posts_comments(n_posts,n_comments,timeperiod)
    c = createClassifier()
    return getOverallValues(c,comments)

if __name__=="__main__":
    initReddit()
    outliers = getDailyOutliers()
    topr = getTopResults()
    #Uncomment this line to not get the twitter posts (it goes faster)
    #c = createClassifier(True)
