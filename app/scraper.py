"""
Pulls tweets from twitter based on a keyword search of popular
tweets. These tweets are filtered using the TextMatcher class in textmatcher.py. 
If these tweets are determined by the model to report police use of force 
they will be input into the a database.
"""
import os

import dataset
import json
import tweepy
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import psycopg2

from app.textmatcher import TextMatcher
from app.training_data import ranked_reports
from app.helper_funcs import tweet_dupes


# import BD url from .env file
load_dotenv()
# make database connection
db = dataset.connect(os.getenv("DB_URL"))

# instantiate TextMatcher class to make category predictions on tweets
model = TextMatcher(ranked_reports)

# import twitter api credential from .env file
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_KEY = os.getenv("ACCESS_KEY")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# make twitter API connection and instantiate connection class using tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# quick DB query statement to run in the function
statement = 'SELECT id_str FROM twitter_potential_incidents ORDER BY id_str DESC LIMIT 1'
# words to ensure are included in the tweet, THIS LIST SHOULD BE EXPANDED.
filter_words = ["police", "officer", "cop"]
# make sure when then tweet runs through the model the tweet receives one of the following ranks,
# If model produces a Rank 0 or 1, it will not be included in the DB
ranked_reports = [
    "Rank 2 - Empty-hand",
    "Rank 3 - Blunt Force",
    "Rank 4 - Chemical & Electric",
    "Rank 5 - Lethal Force",
]


def update_twitter_data(reddit_db):
    """
    Function does not take any variables, functions only purpose to be called when needed.
    This function will pull tweets from twitter that a report police use of force, filter using
    the TextMatcher class, and populate the database.
    """
    # quick database query to see what the id of the last imported tweet was.
    conn = psycopg2.connect(os.getenv("DB_URL"))
    curs = conn.cursor()
    curs.execute(statement)
    conn.commit()
    maxid = curs.fetchall()[0][0]
    curs.close()
    conn.close()

    # loop through through the imported tweets.
    for status in tweepy.Cursor(api.search, q="police", lang='en',
                                result_type='popular', since_id=maxid).items():
        # This assigns a category to the tweet
        category = model(status.text)
        # filters out retweets, tweets that don't include the filter words, and Rank 0 categories
        # tweet_dupes function checks to see if tweet already exists in reddit posts
        conditions = ('RT @' not in status.text) and \
                     any(word in status.text for word in filter_words) \
                     and (category in ranked_reports) \
                     and tweet_dupes(status, reddit_db)
        # imports tweets into the DB
        if conditions:
            description = status.user.description
            loc = status.user.location
            text = status.text
            coords = status.coordinates
            geo = status.geo
            name = status.user.screen_name
            user_created = status.user.created_at
            id_str = status.id_str
            created = status.created_at
            source = status.user.url
            language = status.lang

            if geo is not None:
                geo = json.dumps(geo)

            if coords is not None:
                coords = json.dumps(coords)

            table = db["twitter_potential_incidents"]
            try:
                table.insert(dict(
                    user_description=description,
                    user_location=loc,
                    coordinates=coords,
                    text=text,
                    geo=geo,
                    user_name=name,
                    user_created=user_created,
                    id_str=id_str,
                    created=created,
                    source=source,
                    language=language,
                    category=category,

                    # dummy values to prevent errors when trying to add tweets from the database to the interactive map on the web page
                    city=None,
                    state=None,
                    latitude=None,
                    longitude=None,
                    title=text.split()[:8]
                ))
            except ProgrammingError as err:
                print(err)

    def on_error(self, status_code):
        if status_code == 420:
            # return False if tweepy connection fails
            return False
