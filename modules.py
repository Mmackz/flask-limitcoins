import json
import os
import praw

def authenticate():
   username = os.getenv("praw_USERNAME")
   password = os.getenv("praw_PASSWORD")
   client_id = os.getenv("praw_CLIENT_ID")
   client_secret = os.getenv("praw_CLIENT_SECRET")
   reddit = praw.Reddit(
      username=username,
      password=password,
      user_agent="console:limitcoinsv1.0 (by u/Mcgillby)",
      client_id=client_id,
         client_secret=client_secret
   )
   # reddit = praw.Reddit("ccModBot", user_agent="console:limitcoinsv1.0 (by u/Mcgillby)")
   return reddit

def update(reddit):
   data = json.loads(reddit.subreddit("cryptocurrency").wiki["botconfig/cclimits/data"].content_md)

   with open(os.path.join("static", "data.json"), "w") as f:
      json.dump(data, f, indent=4)
    