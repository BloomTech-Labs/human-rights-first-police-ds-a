""" Twiter Data """
import os
from dotenv import load_dotenv

import psycopg2
from fastapi import APIRouter

load_dotenv()

router =APIRouter()

@router.get('/Twitter')
async def get_Twitter_Data():
    """ Returns all twitter data from database"""
    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # if date_added == None:
    Q = """SELECT * FROM twitter_potential_incidents;"""
    # else:
        # Q = f"""SELECT * FROM police_force WHERE added_on >= '{date_added}';"""
    curs.execute(Q)
    results = curs.fetchall()
    curs.close()
    conn.close()
  
    return results
