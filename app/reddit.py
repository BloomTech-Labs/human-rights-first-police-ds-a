""" Get Reddit Data """
import os
from fastapi import APIRouter
from ast import literal_eval
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.get('/Reddit')
async def get_reddit_data(last_id_added: str = None):
    """ 
    Returns reddit data. \n
    If id is entered all the data greater than that id will be returned. \n
    If no id is entered all the data will be returned.
    """
    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if last_id_added == None:
        Q = """SELECT * FROM police_force;"""
    else:
        Q = f"""SELECT * FROM police_force WHERE id > '{last_id_added}';"""
    curs.execute(Q)
    results = curs.fetchall()
    curs.close()
    conn.close()
  
    # """
    # Convert data to usable json format
    # ### Response
    # dateframe: JSON object
    # """
    for item in results:
        item['links'] = literal_eval(item['links'])
        item['tags'] = literal_eval(item['tags'])
    return results