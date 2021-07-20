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
from app.frankenbert import FrankenBert


# import BD url from .env file
load_dotenv()
# make database connection
db = dataset.connect(os.getenv("DB_URI"))

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
    conn = psycopg2.connect(os.getenv("DB_URI"))
    curs = conn.cursor()
    print('step 1')
    curs.execute("""SELECT tweet_id FROM twitter_incidents_36 ORDER BY tweet_id DESC LIMIT 1""")
    print('step 2')
    #maxid = str(max(0, curs.fetchall()[0][0])) # maxid = str(curs.fetchall()[0][0])
    print('step3')
    #print('maxid: ', maxid)
    curs.close()
    conn.close()

    db = dataset.connect(os.getenv("DB_URI"))
    table = db["twitter_incidents_new"]
    print('connected to table')
    conn = psycopg2.connect(os.getenv("DB_URI"))
    curs = conn.cursor()
    conn.commit()
    for tweet in tweepy.Cursor(api.search, q='police',
                                since_id=1417199914694680577, tweet_mode='extended').items(): # change since_id to 'max_id' once the table is created and populated
        print('we got here')
        # Create a list to avoid processing duplicates
        dupe_check = []

        # filters out retweets / # tweet_dupes function checks to see if tweet already processed \
        # Filters tweets not in english
        conditions = ('RT @' not in tweet.full_text) and \
                     tweet.id_str not in dupe_check \
                     and (tweet.lang == 'en')

        rank_dict = {"1": "Rank 1 - Police Presence", "2": "Rank 2 - Empty-hand",
                     "3": "Rank 3 - Blunt Force", "4": "Rank 4 - Chemical & Electric",
                     "5": "Rank 5 - Lethal Force"}

        if conditions:

            category = get_rank_of_force(tweet.full_text)  # This runs the text of the Tweet through the model
            print('tweet full.text: ', tweet.full_text) # DELETE WHEN DONE DEBUGGING

            dupe_check.append(tweet.id_str)  # Keeps track

            if category != '{"detail":"Not Found"}':
                category_splitted = category.split(': ')
                rank_confidence = category_splitted[1].split(', ')[1].replace('%', '')
                rank_int = int(category_splitted[1].split(', ')[0])  # Gets rank integer for processing
                print('rank_confidence: ', rank_confidence)
                print('type rank_confidence: ', type(rank_confidence))
                print('rank int: ', rank_int)

            else:
                rank_int = 0
            
            if rank_int > 1:
                tweet_id = tweet.id_str
                date_created = tweet.created_at
                user_name = tweet.user.screen_name
                description = tweet.full_text
                force_rank = rank_dict[str(rank_int)]
                confidence = rank_confidence
                tags = TagMaker(tweet.full_text, pb_tags).tags()
                city = None
                state = None
                status = 'pending'
                

                try:
                    table.insert(dict(
                        tweet_id=tweet_id,
                        date_created=date_created,
                        user_name=user_name,
                        description=description,
                        force_rank=force_rank,
                        confidence=confidence,
                        tags=tags,
                        city=city,
                        state=state,
                        status=status
                        ))

                    print('success', tweet.id_str)
                except ProgrammingError as err:
                    print(err)
    curs.close()
    conn.close()

