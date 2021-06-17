""" Initialize tables for Postgres database """
import os

import psycopg2
from dotenv import load_dotenv


def initialize_police_table():
    load_dotenv()
    police_table = """CREATE TABLE IF NOT EXISTS police_force (
        id SERIAL PRIMARY KEY NOT NULL,
        dates TIMESTAMP,
        added_on TIMESTAMP,
        links TEXT,
        case_id TEXT,
        city TEXT,
        state TEXT,
        lat FLOAT,
        long FLOAT,
        title TEXT,
        description TEXT,
        tags TEXT,
        force_rank TEXT
    );"""

    police_table = """CREATE TABLE IF NOT EXISTS twitter_potential_incidents (
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

    police_table = """CREATE TABLE IF NOT EXISTS police_force_updated (
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




    police_table = """CREATE TABLE IF NOT EXISTS in_process (
          id SERIAL PRIMARY KEY NOT NULL,
          original_tweet_id TEXT,
          original_username TEXT,
          original_tweet_text TEXT,
          location FLOAT,
          reply_tweet_id TEXT
      );"""

    police_table = """CREATE TABLE IF NOT EXISTS training (
          id SERIAL PRIMARY KEY NOT NULL,
          tweets TEXT,
          labels TEXT
      );"""

    police_table = """CREATE TABLE IF NOT EXISTS tweets (
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
    curs.execute(police_table)
    conn.commit()
    curs.close()
    conn.close()
