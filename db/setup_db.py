""" Initialize tables for Postgres database """
import psycopg2
import os
from dotenv import load_dotenv
from sql.tables import tables

print('INITIALIZING DATABASE...')


def initialize_db():
    load_dotenv()   

    # Connect to DB and execute create table query
    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()

    print('INITIALIZING TABLES...')
    for table in tables:
        curs.execute(table)

    conn.commit()
    curs.close()
    conn.close()
    print('DONE!')


if __name__ == '__main__':
    initialize_db()