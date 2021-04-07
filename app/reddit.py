""" Get Reddit Data """
import os
from ast import literal_eval

from fastapi import APIRouter
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv


load_dotenv()
router = APIRouter()


@router.get('/Reddit')
async def get_reddit_data(last_id_added: str = None):
    """ 
    Returns reddit data.
    If id is entered all the data greater than that id will be returned.
    If no id is entered all the data will be returned.
    """
    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if last_id_added:
        query = f"""SELECT * FROM police_force WHERE id > '{last_id_added}';"""
    else:
        query = """SELECT * FROM police_force;"""
    curs.execute(query)
    results = curs.fetchall()
    curs.close()
    conn.close()

    # Convert data to usable json format
    for item in results:
        item['links'] = literal_eval(item['links'])
        item['tags'] = literal_eval(item['tags'])
    return results
