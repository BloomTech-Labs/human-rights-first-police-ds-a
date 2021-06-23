"""
Pulls tweets from twitter based on a keyword search of popular
tweets and runs them through the Bert model. If these tweets are
determined by the model to report police use of force they will
be added to the potential_incidents table.

"""
import os

import dataset
import tweepy
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import psycopg2
from app.helper_funcs import get_rank_of_force, clean_data
from app.TagMaker import TagMaker
from app.TagList import pb_tags

# import BD url from .env file
load_dotenv()
# make database connection
db = dataset.connect(os.getenv("DB_URL"))

# make twitter API connection and instantiate connection class using tweepy
auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
auth.set_access_token(os.getenv("ACCESS_KEY"), os.getenv("ACCESS_SECRET"))
api = tweepy.API(auth)

# words to ensure are included in the tweet, THIS LIST SHOULD BE EXPANDED.
filter_words = ["police", "officer", "cop"]


# If model produces a Rank 0 or 1, it will not be included in the DB


def update_twitter_data():
    """
    This function will pull tweets from twitter that report mention the words in the filter words,
    run through the Bert model and populate the database.
    """

    # quick database query to see what the id of the last imported tweet was.
    conn = psycopg2.connect(os.getenv("DB_URL"))
    curs = conn.cursor()
    curs.execute("""SELECT tweet_id FROM incidents ORDER BY tweet_id DESC LIMIT 1""")
    maxid = str(curs.fetchall()[0][0])
    curs.close()
    conn.close()

    db = dataset.connect(os.getenv("DB_URL"))
    table = db["incidents"]
    conn = psycopg2.connect(os.getenv("DB_URL"))
    curs = conn.cursor()
    conn.commit()
    for status in tweepy.Cursor(api.search, q='police',
                                since_id=maxid, tweet_mode='extended').items():

        # Create a list to avoid processing duplicates
        dupe_check = []

        # filters out retweets / # tweet_dupes function checks to see if tweet already processed \
        # Filters tweets not in english
        conditions = ('RT @' not in status.full_text) and \
                     status.id_str not in dupe_check \
                     and (status.lang == 'en')

        rank_dict = {"1": "Rank 1 - Police Presence", "2": "Rank 2 - Empty-hand",
                     "3": "Rank 3 - Blunt Force", "4": "Rank 4 - Chemical & Electric",
                     "5": "Rank 5 - Lethal Force"}

        if conditions:

            category = get_rank_of_force(status.full_text).text  # This runs the text of the Tweet through the model
            dupe_check.append(status.id_str)  # Keeps track

            if category != '{"detail":"Not Found"}':
                rank_int = int(category.split(': ')[0][-1])  # Gets rank integer for processing
                rank_confidence = category.split(': ')[1].replace('%', '').replace('"', '')
            else:
                rank_int = 0

            if rank_int > 1:

                tweet_id = status.id_str
                date_created = status.created_at
                user_name = status.user.screen_name
                twitter_text = status.full_text
                force_rank = rank_dict[str(rank_int)]
                tags = TagMaker(status.full_text, pb_tags).tags()
                city = None
                state = None
                twitterbot_tweet_id = None
                responses = None
                confidence = rank_confidence

                try:
                    table.insert(dict(
                        tweet_id=tweet_id,
                        date_created=date_created,
                        user_name=user_name,
                        twitter_text=twitter_text,
                        force_rank=force_rank,
                        confidence=confidence,
                        tags=tags,
                        city=city,
                        state=state,
                        twitterbot_tweet_id=twitterbot_tweet_id,
                        responses=responses
                        ))

                    print('success', status.id_str)
                except ProgrammingError as err:
                    print(err)
    curs.close()
    conn.close()

