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
    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    curs.execute(police_table)
    conn.commit()
    curs.close()
    conn.close()
