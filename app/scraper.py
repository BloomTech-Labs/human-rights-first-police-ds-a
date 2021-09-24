""" This module holds the Tweepy scraper that scrapes Twitter for incidents """

import datetime as dt

from typing import Dict, List, Tuple

import tweepy
from dotenv import find_dotenv, load_dotenv

from app.db import Database, ForceRanks
from app.franken_bert import FrankenBert
from app.twitter import create_api

load_dotenv(find_dotenv())

DB = Database()

model = FrankenBert("app/saved_model")


def frankenbert_rank(user_input: str) -> Tuple[str, str, Tuple[int, float]]:
    """ Implements Frankenbert for tweet ranking """
    lookup = {
        0: "Rank 0",
        1: "Rank 1",
        2: "Rank 2",
        3: "Rank 3",
        4: "Rank 4",
        5: "Rank 5",
    }
    raw_data = model.predict(user_input)
    rank, conf = raw_data
    return lookup[rank], f"{100 * conf:.2f}%", raw_data


def deduplicate(new_data: List[Dict]) -> List[Dict]:
    """ Checks for duplicates and omits them """
    old_data = DB.get_table(ForceRanks.tweet_id)
    data = []
    for new in new_data:
        if all(new['tweet_id'] != old.tweet_id for old in old_data):
            data.append(new)
    return data


def clean_str(string: str) -> str:
    """ Cleans strings for SQL insertion """
    return string.replace('\n', ' ').replace("'", "’")


def clean_date(date: dt.datetime) -> str:
    """ Cleans date for SQL insertion """
    return date.strftime("%Y-%m-%d")


def scrape_twitter(query: str) -> List[Dict]:
    """ Pull tweets from twitter that report police use of force """
    tweets = []
    api = create_api()
    for status in tweepy.Cursor(
        api.search,
        q=query,
        lang='en',
        tweet_mode="extended",
        count=100,
    ).items(500):
        if 'RT @' not in status.full_text:
            force_str, conf_str, raw_data = frankenbert_rank(status.full_text)
            force_int, conf_float = raw_data
            if force_int > 1 and conf_float > 0.75:
                tweets.append({
                    "incident_date": clean_date(status.created_at),
                    "tweet_id": status.id_str,
                    "user_name": clean_str(status.user.screen_name),
                    "description": clean_str(status.full_text),
                    "force_rank": force_str,
                    "status": "pending",
                    "confidence": conf_float,
                    "tags": "[]",
                    "src": f'["https://twitter.com/{status.user.screen_name}/status/{status.id_str}"]',
                })
    return tweets
