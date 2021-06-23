""" This file holds the schemas to create new tables on database, if necessary.
To create a table change the table value in function on line 51 and run file.
This code should not have to be run unless new (empty) tables have to be generated.
"""
import os

import psycopg2
from dotenv import load_dotenv

def initialize_police_table():
    load_dotenv()
    police_table = """CREATE TABLE IF NOT EXISTS police_force (
    id SERIAL PRIMARY KEY NOT NULL,
    dates TIMESTAMP,
    links TEXT,
    case_id TEXT,
    city TEXT,
    state TEXT,
    title TEXT,
    description TEXT,
    tags TEXT,
    force_rank TEXT,
    confidence TEXT
        );"""

    pi_table = """CREATE TABLE IF NOT EXISTS incidents (
    id SERIAL PRIMARY KEY NOT NULL,
    tweet_id TEXT,
    date_created TIMESTAMP,
    user_name TEXT,
    user_description TEXT,
    twitter_text TEXT,
    force_rank TEXT,
    confidence TEXT,
    tags TEXT,
    city TEXT,
    state TEXT,
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

