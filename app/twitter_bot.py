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
    # get_mentions() returns a list of tweet objects
    # get_mentions() has a parameter of the last tweet id for mentions that has been processed
    # This is important to keep track of which mentions the bot has already seen
    # The list start with the most current tweet and ends with the oldest tweet it finds, they are in descending order
    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = "SELECT user_name FROM dummy_table WHERE tweet_id = 'update id';"
    curs.execute(query)
    last_reply_id = curs.fetchone()
    last_reply_id = last_reply_id['user_name']
    last_id = []
    for x in get_mentions(last_reply_id):
        received_reply(x, curs)
        if last_id == []:
            last_id.append(x.id_str)
    last_id = last_id.pop()

    query = f"UPDATE dummy_table set user_name = '{last_id}' WHERE tweet_id = 'update id';"
    curs.execute(query)
    conn.commit()
    curs.close()
    conn.close()
    return None


def received_reply(tweet, curs):
    reply_id = tweet.in_reply_to_status_id_str
    response_text = tweet.full_text
    query = f"SELECT responses FROM dummy_table WHERE twitterbot_tweet_id = '{reply_id}';"
    curs.execute(query)
    responses = curs.fetchone()['responses']
    if responses == None:
        responses = ""
    list_of_tweets = string_to_list(responses, response_text)
    new_str = list_to_string(list_of_tweets)
    query = f"UPDATE dummy_table set responses = '{new_str}' WHERE twitterbot_tweet_id = '{reply_id}';"
    curs.execute(query)
    return


def send_bot_tweet(tweet, text):
    username = tweet.user.screen_name
    reply_id = tweet.id_str
    sent_tweet = api.update_status(status=f"@{username} {text}", in_reply_to_status_id=reply_id, tweet_mode='extended')
    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = f"UPDATE dummy_table set twitterbot_tweet_id = '{sent_tweet.id_str}' WHERE tweet_id = '{reply_id}';"
    curs.execute(query)
    conn.commit()
    conn.close()
    curs.close()
    return sent_tweet


def string_to_list(str, append=""):
    str_list = str.split(":.:.:")
    if str_list[-1] == "":
        str_list.pop()
    if append != "":
        str_list.append(append)
    return str_list


def list_to_string(lst):
    new_str = ""
    for x in lst:
        new_str += x + ":.:.:"
    return new_str[:-5]
