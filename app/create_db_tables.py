""" Initialize tables for Postgres database """
import os

import psycopg2
from dotenv import load_dotenv
load_dotenv()

def initialize_police_table():


    pi_table = """CREATE TABLE IF NOT EXISTS potential_incidents (
          tweet_id PRIMARY KEY NOT NULL,
          date_created TIMESTAMP,
          user_name TEXT,
          user_description TEXT,
          user_location TEXT,
          twitter_text TEXT,
          date_created TIMESTAMP, 
          source TEXT,
          category TEXT,
          city TEXT,
          state TEXT,
          lat FLOAT,
          lon FLOAT,
          title TEXT,
          twitterbot_tweet_id TEXT,
          responses TEXT
      );"""

    pfu_table = """CREATE TABLE IF NOT EXISTS police_force_updated (
          id SERIAL PRIMARY KEY NOT NULL,
          dates TIMESTAMP,
          links TEXT,
          case_id TEXT,
          city TEXT,
          state TEXT,
          lat FLOAT,
          lon FLOAT,
          title TEXT,
          description TEXT,
          tags TEXT,
          force_rank TEXT
          confidence FLOAT
      );"""




    ip_table = """CREATE TABLE IF NOT EXISTS in_process (
          id SERIAL PRIMARY KEY NOT NULL,
          original_tweet_id TEXT,
          original_username TEXT,
          original_tweet_text TEXT,
          location FLOAT,
          reply_tweet_id TEXT
      );"""

    training_table = """CREATE TABLE IF NOT EXISTS training (
          id SERIAL PRIMARY KEY NOT NULL,
          tweets TEXT,
          labels TEXT
      );"""

    tweets_table = """CREATE TABLE IF NOT EXISTS tweets (
          id SERIAL PRIMARY KEY NOT NULL,
          user_description TEXT,
          user_location TEXT,
          coordinates NULL,
          text TEXT,
          geo NULL,
          user_name TEXT,
          user_created TIMESTAMP,
          id_str FLOAT,
          created TIMESTAMP,
          source TEXT,
          language TEXT
      );"""

    db_url = 'postgresql://djxbobov:66rP3cmBEgw6EHiw45PJds9X-ji8nNZc@queenie.db.elephantsql.com:5432/djxbobov'
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    curs.execute(pi_table)
    conn.commit()
    curs.close()
    conn.close()


