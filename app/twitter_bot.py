import tweepy
import pandas as pd
from dotenv import load_dotenv
import os
import psycopg2
import psycopg2.extras
load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY2")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET2")
ACCESS_KEY = os.getenv("ACCESS_KEY2")
ACCESS_SECRET = os.getenv("ACCESS_SECRET2")
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)
try:
    api.verify_credentials()
    print('Authorized')
except:
    print('Error during authentication')


def get_mentions(since_id):
    return api.mentions_timeline(since_id = since_id, tweet_mode = 'extended')


def twitter_reply(reply_id, username, text):
    if text == "":
        reply_text = '''
        ------- test -------
        We noticed that you are reporting a police incident.
        '''
    else:
        reply_text = text

    tweet = api.update_status(status=f"@{username} {reply_text}", in_reply_to_status_id=reply_id, tweet_mode='extended')
    return tweet


def direct_message(username):
    user = api.get_user(username)
    message = '''
    Just testing some features.
    This sends a direct message to the person
    '''
    api.send_direct_message(user.id, message)
    return 'direct message sent'


def update_mentions():
    # get_mentions() returns a list of tweet objects that "@twitterbot" in their status as a reply.
    # The loop starts with most recent tweet and moves towards old tweets that do not need to be updated.
    # The loops stops when it gets to tweets it has seen before.
    db_url = 'postgresql://djxbobov:66rP3cmBEgw6EHiw45PJds9X-ji8nNZc@queenie.db.elephantsql.com:5432/djxbobov'
    conn = psycopg2.connect(db_url)
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = "SELECT original_tweet_id FROM in_process WHERE id = 1;"
    curs.execute(query)
    results = curs.fetchall().split(" ")
    last_reply_id = results[-1]
    last_id = []
    for x in get_mentions(last_reply_id):
        sent_tweet = received_reply(x, curs)

        #need to use sent_tweet to update DataBase - needs to be done

        if last_id == []:
            last_id.append(x.id_str)
    last_id = last_id.pop()
    results.pop()
    results.append(last_id)
    new_str = ""
    for x in results:
        new_str += str(x)
    query = f"UPDATE in_process set original_tweet_id = {new_str} WHERE id = 1"
    curs.execute(query)
    curs.close()
    conn.close()
    return None


def received_reply(tweet, curs):
    reply_id = tweet.in_reply_to_status_id_str
    response_text = tweet.full_text
    query = f"UPDATE in_process set location = {response_text} WHERE reply_tweet_id = {reply_id}"
    curs.execute(query)
    return


def send_bot_tweet(tweet, text):
    username = tweet.user.screen_name
    reply_id = tweet.id_str
    sent_tweet = api.update_status(status=f"@{username} {text}", in_reply_to_status_id=reply_id, tweet_mode='extended')
    return sent_tweet

#update_mentions()

# table column names [id, original_tweet_id, original_username, original_tweet_text, location, reply_tweet_id]