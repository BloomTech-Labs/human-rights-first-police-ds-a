""" Functions used to process reddit data """
import os
import datetime

import pandas as pd
import numpy as np
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras

from app.training_data import ranked_reports
from app.textmatcher import TextMatcher


load_dotenv()

model = TextMatcher(ranked_reports)


def check_new_items(db_info, api_info):
    """ Find the number of new items on the API """
    new_items = []
    for item in api_info['data']:
        if not any(d['case_id'] == item['id'] for d in db_info):
            new_items.append(item)
    return new_items


def cleanLinks(url_col):
    """ Convert links from json to a str. Creates hyperlink"""
    links_out = []
    for link in url_col:
        links_out.append(link['url'])
    return links_out


def getRankOfForce(text):
    return model(text)


def getLatandLon(i, item, df):
    if item != '':
        item = item.split(',')
        df.at[i, 'lat'] = float(item[0])
        df.at[i, 'long'] = float(item[1])


def getValues(item):
    current_dt = datetime.datetime.today()
    return (item['date'], current_dt, str(item['links']), str(item['id']),
            str(item['city']), str(item['state']), item['lat'], item['long'],
            str(item['title']), str(item['description']), str(item['tags']),
            item['force_rank'])


def loadData():
    """ Get all incidents stored in database """
    DB_CONN = os.getenv('DB_URL')
    pg_conn = psycopg2.connect(DB_CONN)
    pg_curs = pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    Q = """SELECT * FROM police_force;"""
    pg_curs.execute(Q)
    results = pg_curs.fetchall()
    pg_curs.close()
    return results


def insertData(data):
    """ Insert data into police_force table """
    DB_CONN = os.getenv("DB_URL")
    pg_conn = psycopg2.connect(DB_CONN)
    pg_curs = pg_conn.cursor()
    pb2020_insert_query = """
    INSERT INTO police_force 
    (date,added_on, links, case_id, city, state,lat,long, 
    title, description, tags, force_rank)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    for item in data:
        pg_curs.execute(pb2020_insert_query, getValues(item))
    pg_conn.commit()
    pg_curs.close()
    pg_conn.close()
    return


def preprocessNewData(new_data_json):
    """
    Preprocessing function to mimic the output of the initial dataframe.
    """
    df = pd.DataFrame(data=new_data_json)

    # Rename columns/ Drop irrelevant columns
    df = df.rename(columns={'name': 'title'}).drop(
        labels=['edit_at', 'date_text'], axis=1)

    # Reorder column headers
    df = df[
        ['date', 'links', 'id', 'city', 'state', 'geolocation', 'title', 'tags',
         'description']]

    # Update the "date" column to timestamps
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df['date'] = df.date.astype(object).where(df.date.notnull(), None)
    df = df.sort_values(by='date')
    df.reset_index(inplace=True)
    df['description'] = df['description'].replace({np.NaN: "None"})

    # Create placeholders for latitude (lat) and longitude (lon) columns.
    df['lat'] = pd.Series(np.zeros(df.shape[0], dtype=float))
    df['long'] = pd.Series(np.zeros(df.shape[0], dtype=float))

    # Populate lat and lon columns
    for i, row in enumerate(df['geolocation']):
        getLatandLon(i, row, df)

    df = df.drop(labels=['geolocation', 'index'], axis=1)
    df['links'] = df['links'].apply(cleanLinks)
    df['force_rank'] = df['title'].apply(getRankOfForce)
    return df.to_dict(orient='records')


def tweet_dupes(tweet, reddit_db):
    tweet_url = "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str

    for url in reddit_db[3]:
        if url == tweet_url:
            return False

    return True


def reddit_dupes():
    DB_CONN = os.getenv("DB_URL")
    pg_conn = psycopg2.connect(DB_CONN)
    pg_curs = pg_conn.cursor()

    for url in reddit_db['links']:
        if "twitter.com/" and "/status/" in url:
            sliced_id = url.split('/')[:-1]
            reddit_delete_query = """
            DELETE FROM twitter_potential_incidents
            WHERE id_str = """ + sliced_id
            pg_curs.execute(reddit_delete_query)

    pg_conn.commit()
    pg_curs.close()
    pg_conn.close()
