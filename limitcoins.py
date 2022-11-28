import json
import math
import os
import praw
import re
import requests
import threading
from coinlist import coinlist

def authenticate():
    username = os.getenv('praw_USERNAME')
    password = os.getenv('praw_PASSWORD')
    client_id = os.getenv('praw_CLIENT_ID')
    client_secret = os.getenv('praw_CLIENT_SECRET')
    reddit = praw.Reddit(
       username=username,
       password=password,
       user_agent="console:limitcoinsv1.0 (by u/Mcgillby)",
       client_id=client_id,
       client_secret=client_secret
    )
   #  reddit = praw.Reddit("ccModBot", user_agent="console:limitcoinsv1.0 (by u/Mcgillby)") 
    return reddit

reddit = authenticate()
subreddit = reddit.subreddit("cryptocurrency")
first_run = 1
limits = {"error": "there was an error retrieving the data.. try again later"}
    
def purify_list(plist):
    try:
        mods = list(subreddit.moderator())
        approved_flairs = ['ama', 'official', 'megathread', 'event']
        newlist = [x for x in plist if not (x.stickied or str(x.link_flair_text).lower() in approved_flairs 
                                    or str(x.link_flair_text).lower().endswith('*') or x.author in mods)]
    except:
        global limits
        limits = {"error": "there was an error retrieving the data.. try again later"}
        newlist = []

    return newlist


def extract_coins(post):
    # Split title into individual words greater than 2 letters (or 2 letters in allcaps)  
    split = (list(filter(lambda x: (len(x) > 2 and not x.isdigit()) or (len(x) == 2 
        and x.isupper() and x.isalpha()), set(re.split(r'\W', post.title)))))

    # Logic to deal with coin names that contain spaces
    fullnames = [coin for item in coinlist for coin in item if ' ' in coin ]
    for coinname in fullnames:
        if coinname in post.title:
            split.append(coinname)

    # Search for matches
    matches = []
    for word in split:
        for coin in coinlist:
            if word in coin:
                matches.append((coin[0], post.id, post.created_utc, post.title))

    matches = list(set(matches))
    return matches


def get_limits():
    # get total marketcap from coingecko api
    total_cap = get_totalmcap() 

    # return false if marketcap api call fails
    if not total_cap:
        return False

    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': '10',
        'page': '1',
        'sparkline': 'false'
    }
    try:
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets', params=params).json()
        if 'error' in response:
            raise Exception(response['error'])
    except Exception as error:
        print("ERROR: ", error)
        return False

    mapped = map(lambda x: {'symbol': x['symbol'].upper(),
         'limit': num_posts(x['market_cap'] / total_cap)}, response)

    data = list(filter(lambda x: x['limit'] > 2, mapped))
    return data


def get_posts():
    try:
        posts = purify_list(subreddit.hot(limit=50))
    except:
        return []
    return posts

def get_totalmcap():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/global').json()
        if 'error' in response:
            raise Exception(response['error'])
        total_mcap = response['data']['total_market_cap']['usd']
    except Exception as error:
        print("ERROR: ", error)
        total_mcap = 0
    return round(total_mcap)


def limit_coins():
    global first_run
    global limits
    all_matches = []

    posts = get_posts()

    # get limits and start interval to update limits every day
    if first_run:
        new_limits = get_limits()
        if new_limits:
            limits = new_limits
        update_limits(get_limits)
        first_run = 0

    if not posts or not limits:
        limits = {"error": "there was an error retrieving the data.. try again later"}
        write_json("static", "data.json", limits)

    if not "error" in limits:
        for post in posts:
            # Check if post has COMEDY flair
            if post.link_flair_text == 'COMEDY':
                all_matches.append(('COMEDY FLAIR', post.id, post.created_utc, post.title));
            else:
                # Search post for coin mentions
                matches = extract_coins(post)
                for item in matches:
                    all_matches.append(item)

        coins = set()
        for match in all_matches:
            coins.add(match[0])

        coins = list(sorted(coins))

        coins_at_limit = []

        coin_posts = {}

        for coin in coins:
            # set coin limit
            coin_item = next((x for x in limits if x['symbol'] == coin), {})
            if coin_item:
                limit = coin_item['limit']
            else:
                limit = 2

            # seperate specific coin matches from all_matches
            coin_matches = list(filter(lambda x: x[0] == coin, all_matches))

            coin_posts[coin] = coin_matches

            # remove all posts passed the limit
            if len(coin_matches) >= limit:

                coins_at_limit.append(coin)
                continue
        
        data = {"limits": limits, "coins": coins_at_limit, "posts": coin_posts}
        write_json("static", "data.json", data)

def write_json(target_path, target_file, data):
    with open(os.path.join(target_path, target_file), 'w') as f:
        json.dump(data, f, indent=4)


def num_posts(ratio):
    return math.floor(10 * ratio * (1 + ratio**-0.7))


# updates limits once per day
def update_limits(func):
    def wrapper():
        update_limits(func)
        global limits
        val = func()
        if val:
            limits = val
    t = threading.Timer(86400, wrapper)
    t.start()
    return

