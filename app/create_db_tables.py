""" Initialize tables for Postgres database """
import os

import psycopg2
from dotenv import load_dotenv
load_dotenv()

def initialize_police_table():

    commands = (
    """CREATE TABLE IF NOT EXISTS police_force (
        id SERIAL PRIMARY KEY NOT NULL,
        dates TIMESTAMP,
        links TEXT,
        case_id TEXT,
        city TEXT,
        state TEXT,
        lat FLOAT,
        long FLOAT,
        title TEXT,
        description TEXT,
        tags TEXT,
        force_rank TEXT,
        confidence FLOAT
    )""",

    """CREATE TABLE IF NOT EXISTS in_process (
        id SERIAL PRIMARY KEY NOT NULL,
        original_tweet_id TEXT,
        original_username TEXT,
        original_tweet_text TEXT,
        location TEXT,
        reply_tweet_id TEXT
    );"""
    )


    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    for command in commands:
        curs.execute(command)
    conn.commit()
    curs.close()
    conn.close()


