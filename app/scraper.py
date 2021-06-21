"""
Pulls tweets from twitter based on a keyword search of popular
tweets and runs them through the Bert model. If these tweets are
determined by the model to report police use of force they will
be added to the potential_incidents table.

"""
import os

import dataset
import json
import tweepy
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import psycopg2
from app.helper_funcs import getRankOfForce, clean_data


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
    curs.execute("""SELECT tweet_id FROM potential_incidents ORDER BY tweet_id DESC LIMIT 1""")
    conn.commit()
    maxid = str(curs.fetchall()[0][0])
    print(maxid)
    curs.close()
    conn.close()

   
    db = dataset.connect(os.getenv("DB_URL"))
    table = db["potential_incidents"]
    conn = psycopg2.connect(os.getenv("DB_URL"))
    curs = conn.cursor()
    conn.commit()
    for status in tweepy.Cursor(api.search, q='police',
                                since_id=maxid, tweet_mode='extended').items():

        ## Create a list to avoid processing duplicates
        dupe_check = []

        # filters out retweets / # tweet_dupes function checks to see if tweet already processed \
        # Filters tweets not in english
        conditions = ('RT @' not in status.full_text) and \
                     status.id_str not in dupe_check \
                     and (status.lang=='en')

        if conditions:

            category = getRankOfForce(clean_data(status.full_text)).text    # This runs the text of the Tweet through the model
            dupe_check.append(status.id_str)  # Keeps track


            if category != '{"detail":"Not Found"}':
                rank_int = int(category.split(': ')[0][-1])                  # Gets rank integer for processing
                rank_confidence = category.split(': ')[1].replace('%', '').replace('"', '')
            else:
                rank_int = 0


            if rank_int > 1:

                tweet_id = status.id_str
                date_created = status.created_at
                user_name = status.user.screen_name
                user_location = status.user.location
                twitter_text = status.full_text
                source = status.user.url
                category = rank_int
                city = None
                state = None
                lat = None
                long = None
                title = None
                twitterbot_tweet_id = None
                responses = None
                confidence = rank_confidence



                try:
                    table.insert(dict(
                        tweet_id=tweet_id,
                        date_created=date_created,
                        user_name=user_name,
                        user_location=user_location,
                        twitter_text=twitter_text,
                        source=source,
                        category=category,
                        city=city,
                        state=state,
                        lat=lat,
                        long=long,
                        title=title,
                        twitterbot_tweet_id=twitterbot_tweet_id,
                        responses=responses,
                        confidence=confidence))


                    print('success', status.id_str)
                except ProgrammingError as err:
                    print(err)
    curs.close()
    conn.close()


