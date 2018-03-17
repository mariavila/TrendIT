from Constants import *
import requests
import requests.auth
from threading import Timer
import json
from time import sleep

token = None
headers = None


def main():
    params = {
        "t": "day",
        "limit": 1
    }
    response = requests.get("https://oauth.reddit.com/r/all/top", headers=headers, params=params).json()
    # print(response)
    # print(json.dumps(response, indent=4, sort_keys=False))
    for post in [a["data"] for a in response["data"]["children"]]:
        print(post["title"])
        postId = post["id"]
        sub = post["subreddit"]
        params={
            "depth": 3,
            "limit": 100,
            "sort": "top"
        }
        response_post = requests.get("https://oauth.reddit.com/r/%s/comments/%s" % (sub, postId), headers=headers).json()
        for comment in [a["data"] for a in response_post[1]["data"]["children"][:-1]]:
            print(comment["body"])
            print("---")


def refresh_token():
    global token, headers
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "refresh_token",
                 "refresh_token": REFRESH_TOKEN}
    headers = {"User-agent": USER_AGENT}
    response = requests.post(API + "access_token",
                             auth=client_auth,
                             data=post_data,
                             headers=headers)
    token_json = response.json()
    token = token_json["access_token"]
    headers = {"Authorization": "bearer " + token,
               "User-agent": USER_AGENT}

    refresh = Timer(3500, refresh_token)
    refresh.setDaemon(True)
    refresh.start()


if __name__ == "__main__":
    refresh_token()
    main()
