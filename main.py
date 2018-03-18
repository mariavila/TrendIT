import sys
import os
import csv

import GetTop10
from sentimentAnalysis import createClassifier,Classify
from makeSubredditPredictions import SubredditProbability
subreditCateg = {}
c = createClassifier()
def loadDictionary():
    filename = "subredditCategories.csv"
    full_path = filename
    for path in sys.path:
        full_path = os.path.join(path, filename)
        if os.path.isfile(str(full_path)):
            break
    if not os.path.isfile(full_path):
        print ("WARNING : Not found")
        return {}
    else:
        d = {}
        fp = open( full_path, 'rb' )
        reader = csv.reader( fp, delimiter=',', quotechar='"', escapechar='\\' )

        for row in reader:
            d[row[0]] = row[1]
        return d

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
    d = {}
    for i in range (len (subredNames)):
        if subredNames[i] in d.keys():
            d[subredNames[i]] += subredits[i]["upvotes"]
        else :
            d[subredNames[i]] = subredits[i]["upvotes"]
    return d
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
    posts = GetTop10.get_top_posts_comments(n_posts,n_comments,timeperiod)
    return getOverallValues(c,posts)

def getTopResultsByCategory (category,n_posts=100,n_comments=50, timeperiod = "day"):
    posts = GetTop10.get_top_posts_comments(n_posts,n_comments,timeperiod)
    posts = filter (lambda p : getCategory(p["sub"])==category.lower(), posts)
    if len (posts)>0:
        return getOverallValues(c,posts)
    else :
        print ("WARNING : wrong category : "+category)
        return []


def getMostPopularCategories (n_posts =100,timeperiod="day"):
    posts = GetTop10.get_top_posts_subreddits(n_posts,timeperiod)
    cats = {}
    for p in posts :
        current_category = getCategory(p["sub"])
        if current_category in cats.keys():
            cats[current_category] += p["upvotes"]
        else:
            cats[current_category] = p["upvotes"]
    return cats

def getCategory (subreddit):
    subreditCateg = loadDictionary()
    if subreddit in subreditCateg.keys():
        return subreditCateg[subreddit].lower()
    else :
        return "other"
def getCategoriesList ():
    l = []
    subreditCateg = loadDictionary()
    for word in subreditCateg.keys():
        if not subreditCateg[word] in l:
            l.append(subreditCateg[word])
    return l
if __name__=="__main__":
    initReddit()
    print (getTopSubredits())
    outliers = getDailyOutliers()
    topr = getTopResults()

    #Uncomment this line to not get the twitter posts (it goes faster)
    #c = createClassifier(True)
