""" This file holds the schemas to create new tables on database, if necessary.
To create a table change the table value in function on line 51 and run file.
This code should not have to be run unless new (empty) tables have to be generated.
"""
import os

import psycopg2
from dotenv import load_dotenv


def initialize_police_table():
    load_dotenv()

    pi_table = """CREATE TABLE IF NOT EXISTS final_test (
    incident_id SERIAL PRIMARY KEY NOT NULL,
    incident_date TIMESTAMP NOT NULL,
    tweet_id TEXT,
    user_name TEXT,
    description VARCHAR(10000) NOT NULL,
    city TEXT,
    state TEXT,
    lat FLOAT,
    long FLOAT,
    title TEXT,
    force_rank TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    confidence FLOAT,
    tags TEXT,
    src VARCHAR(8000)
          );"""


    db_url = os.getenv('DB_URI')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    curs.execute(pi_table)
    conn.commit()
    curs.close()
    conn.close()
