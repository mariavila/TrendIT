import sys
sys.path.append("Reddit API")
import GetTop10
from sentimentAnalysis import createClassifier,Classify
def main ():
    GetTop10.refresh_token()
    return GetTop10.get_top_posts()


if __name__=="__main__":
    comments = main()
    print (len (comments))
    classifier = createClassifier()
    for d in comments:
        print ("*************************************")
        #print (d)

        print (Classify(d["title"],classifier))
        for com in d["comments"]:
            print (com,Classify(com["body"],classifier))
