""" Initialize tables for Postgres database """
import psycopg2
import os
from dotenv import load_dotenv

print('DESTROYING TABLES...')


def destroy_db():
    load_dotenv()   

    # Connect to DB and execute create table query
    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()

    tables = [
        'police_force',
        'twitter_potential_incidents',
    ]

    for table in tables:
        print(f'DROPPING {table}')
        curs.execute(f'DROP TABLE {table}')
        conn.commit()

    curs.close()
    conn.close()
    print('DONE!')


if __name__ == '__main__':
    destroy_db()