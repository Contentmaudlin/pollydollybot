import logging
import tweepy
import os
from datetime import datetime, timezone, timedelta
import random

import azure.functions as func

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

user_id = os.environ["userid"]

api = tweepy.Client(bearer_token=BEARER_TOKEN,
                    access_token=ACCESS_TOKEN,
                    access_token_secret=ACCESS_TOKEN_SECRET,
                    consumer_key=CONSUMER_KEY,
                    consumer_secret=CONSUMER_SECRET)

def meggie():
    ecount = random.randint(1, 4)
    exclamationcount = random.randint(2, 5)

    meggieStr = "meggi" + ecount * "e" + exclamationcount*"!"
    if random.random() < 0.2:
        meggieStr += " i love "
        youRand = random.randint(1, 3)
        if youRand == 1:
            meggieStr += "youu!"
        elif youRand == 2:
            meggieStr += "yu!"
        elif youRand == 3:
            meggieStr += "youuu!!!!" 
        else:
            meggieStr += "u!!!"
    
    return meggieStr

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(user_id)

    threeMinutesAgoDatetime = datetime.now(timezone.utc) - timedelta(minutes=3)
    queryStr = " from: " + user_id
    recentTweets = api.search_recent_tweets(query=queryStr, start_time=threeMinutesAgoDatetime, expansions=['referenced_tweets.id'])
    if recentTweets.data is not None:
        for tweet in recentTweets.data:
            id = tweet['id']
            if tweet['referenced_tweets'] is None:
                logging.info('replying to tweet: ' + str(id))
                api.create_tweet(text=meggie(), in_reply_to_tweet_id=id)
            else:
                logging.info('ignor bcuz its rt')

    logging.info('bai!')
    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )
