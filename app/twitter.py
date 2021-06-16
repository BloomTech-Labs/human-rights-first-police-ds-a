""" Twitter Data """
import os

from fastapi import APIRouter
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras

load_dotenv()

router = APIRouter()


@router.get('/Twitter')
async def get_twitter_data(last_id_added: str = None):
    """ 
    Returns twitter data. \n
    If id is entered all the data greater than that id will be returned. \n
    If no id is entered all the data will be returned.
    """
    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if last_id_added:
        query = f"SELECT * FROM twitter_potential_incidents WHERE id > '{last_id_added}';"
    else:
        query = "SELECT * FROM twitter_potential_incidents;"
    curs.execute(query)
    results = curs.fetchall()
    curs.close()
    conn.close()
    return results

def get_twitter_data_test(last_id_added: str = None):
    """
    Returns twitter data. \n
    If id is entered all the data greater than that id will be returned. \n
    If no id is entered all the data will be returned.
    """
    db_url = 'postgresql://djxbobov:66rP3cmBEgw6EHiw45PJds9X-ji8nNZc@queenie.db.elephantsql.com:5432/djxbobov'
    conn = psycopg2.connect(db_url)
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = "SELECT * FROM in_process;"
    curs.execute(query)
    results = curs.fetchall()
    curs.close()
    conn.close()
    return results

for x in get_twitter_data_test():
    print(x)

tables = ['knex_migrations', 'knex_migrations_lock', 'incidents', 'twitter_incidents', 'profiles', 'police_force']