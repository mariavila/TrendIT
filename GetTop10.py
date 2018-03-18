from Constants import *
import requests
import requests.auth
from threading import Timer
import json
from time import sleep

token = None
headers = None


def get_top_posts_comments(n_posts=10, n_comments=50, time_period="day"):

    time_period = time_period.lower()

    if n_posts > 100:
        raise NotImplementedError("More than 100 posts not implemented")
    if n_posts < 1:
        raise ValueError("n_posts can't be lower than 1")
    if n_comments < 1:
        raise ValueError("n_comments can't be lower than 1")
    allowed = ("hour", "day", "week", "month", "year", "all")
    if time_period not in allowed:
        raise ValueError("time_period has to be one of the following:\n%s" % ", ".join(allowed))

    params = {
        "t": time_period,
        "limit": n_posts
    }
    response = requests.get("https://oauth.reddit.com/r/all/top", headers=headers, params=params).json()
    posts = []
    for post in [a["data"] for a in response["data"]["children"]]:
        title = post["title"]
        post_id = post["id"]
        sub = post["subreddit"]
        post_upvotes = post["ups"]
        params = {
            "depth": 3,
            "limit": n_comments,
            "sort": "top"
        }
        response_post = requests.get("https://oauth.reddit.com/r/%s/comments/%s" % (sub, post_id),
                                     headers=headers, params=params).json()
        comments = get_comment_data(response_post[1])
        posts.append({"title": title, "upvotes": post_upvotes, "comments": comments,"sub":sub})

    return posts


def get_comment_data(parent):
    comments = []
    for comment in parent["data"]["children"]:
        if comment["kind"] == "t1":
            text = comment["data"]["body"]
            upvotes = comment["data"]["ups"]

            comments.append({"upvotes": upvotes, "body": text})
            if len(comment["data"]["replies"]) > 0:
                comments.extend(get_comment_data(comment["data"]["replies"]))
    return comments


def get_top_posts_subreddits(n_posts=100, time_period="day"):
    if n_posts > 100:
        raise NotImplementedError("More than 100 posts not implemented")
    if n_posts < 1:
        raise ValueError("n_posts can't be lower than 1")
    allowed = ("hour", "day", "week", "month", "year", "all")
    if time_period not in allowed:
        raise ValueError("time_period has to be one of the following:\n%s" % ", ".join(allowed))

    params = {
        "t": time_period,
        "limit": n_posts
    }
    response = requests.get("https://oauth.reddit.com/r/all/top", headers=headers, params=params).json()
    posts = []
    for post in [a["data"] for a in response["data"]["children"]]:
        sub = post["subreddit"]
        post_upvotes = post["ups"]
        posts.append({"sub": sub, "upvotes": post_upvotes})
    return posts


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
    print(get_top_posts_subreddits(10))
