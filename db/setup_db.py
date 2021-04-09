""" Initialize tables for Postgres database """
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sql.tables import tables
from sql.data import POLICE_FORCE_INSERT, TWITTER_POTENTIAL_INCIDENTS_INSERT

print('INITIALIZING DATABASE...')

reddit_data = pd.read_csv('../static/reddit_data.csv')
reddit_data = reddit_data.fillna(value='')
twitter_data = pd.read_csv('../static/potential_incidents.csv')
twitter_data = twitter_data.fillna(value='')

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


    print('INITIALIZING REDDIT DATA...')
    length, current = len(reddit_data), 1  # These are used for status updates.
    for _, row in reddit_data.iterrows():
        _, _, dates, added_on, link, case_id, city, state, lat, lng, title, description, tags, force_rank = row
        
        if not dates: continue  # Null dates on insert break things.
        
        curs.execute(POLICE_FORCE_INSERT, (dates, added_on, link, case_id, city, 
                                           state, lat, lng, title, description, 
                                           tags, force_rank))

        # Status update print out.                                           
        if current % 100 == 0:
            precentage_complete = round((current / length) * 100, 2)
            padding = ' ' * (7 - len(str(precentage_complete)))
            print(f'{precentage_complete}%{padding}COMPLETED')
        current += 1


    print('INITIALIZING TWITTER DATA...')
    length, current = len(twitter_data), 1
    for _, row in twitter_data.iterrows():
        _, user_description, user_location, coordinates, text, geo, user_name, user_created, id_str, created, source, language, category = row
        curs.execute(TWITTER_POTENTIAL_INCIDENTS_INSERT, (user_description, user_location, coordinates, text, geo, user_name, user_created, id_str, created, source, language, category))

        # Status update print out.                                           
        if current % 100 == 0:
            precentage_complete = round((current / length) * 100, 2)
            padding = ' ' * (7 - len(str(precentage_complete)))
            print(f'{precentage_complete}%{padding}COMPLETED')
        current += 1

    conn.commit()
    curs.close()
    conn.close()
    print('DONE!')


if __name__ == '__main__':
    initialize_db()