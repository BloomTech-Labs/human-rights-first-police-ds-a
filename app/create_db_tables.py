""" Initialize tables for Postgres database """
import os

import psycopg2
from dotenv import load_dotenv


def initialize_police_table():
    #load_dotenv()
    police_table = """CREATE TABLE IF NOT EXISTS police_force (
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
        force_rank TEXT,
        confidence FLOAT
    );"""

    pi_table = """CREATE TABLE IF NOT EXISTS incidents (
          tweet_id TEXT PRIMARY KEY NOT NULL,
          date_created TIMESTAMP,
          user_name TEXT,
          user_description TEXT,
          twitter_text TEXT, 
          title TEXT,
          source TEXT,
          category TEXT,
          confidence FLOAT,
          city TEXT,
          state TEXT,
          lat FLOAT,
          lon FLOAT,
          tags TEXT,
          twitterbot_tweet_id TEXT,
          responses TEXT
      );"""

    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    curs.execute(pi_table)
    conn.commit()
    curs.close()
    conn.close()

