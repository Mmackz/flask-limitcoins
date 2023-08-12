import json
import os
import praw
import logging

def authenticate():
    try:
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
        logging.info("Authenticated successfully with Reddit.")
        return reddit
    except Exception as e:
        logging.error(f"Error authenticating with Reddit: {str(e)}")
        raise e

def update(reddit):
    try:
        data = json.loads(reddit.subreddit("cryptocurrency").wiki["botconfig/cclimits/data"].content_md)
        with open(os.path.join("static", "data.json"), "w") as f:
            json.dump(data, f, indent=4)
        logging.info("Data updated successfully.")
    except Exception as e:
        logging.error(f"Error updating data: {str(e)}")
        raise e
