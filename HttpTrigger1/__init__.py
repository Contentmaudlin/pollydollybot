import logging
import tweepy
import os
from datetime import datetime, timezone, timedelta

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

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(user_id)

    threeMinutesAgoDatetime = datetime.now(timezone.utc) - timedelta(minutes=3)
    queryStr = "from: " + user_id
    recentTweets = api.search_recent_tweets(query=queryStr, start_time=threeMinutesAgoDatetime)
    if recentTweets.data is not None:
        for tweet in recentTweets.data:
            print(tweet)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
            logging.info(req_body)
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
