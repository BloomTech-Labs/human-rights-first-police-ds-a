""" Twiter Data """
import os
from fastapi import APIRouter
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras

load_dotenv()

router =APIRouter()

@router.get('/Twitter')
async def get_reddit_data(last_id_added: str = None):
    """ 
    Returns twitter data. \n
    If id is entered all the data greater than that id will be returned. \n
    If no id is entered all the data will be returned.
    """
    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if last_id_added == None:
        Q = """SELECT * FROM twitter_potential_incidents;"""
    else:
        Q = f"""SELECT * FROM twitter_potential_incidents WHERE id > '{last_id_added}';"""
    curs.execute(Q)
    results = curs.fetchall()
    curs.close()
    conn.close()
  
    return results
