""" Get Reddit Data """
from fastapi import APIRouter
from ast import literal_eval
import pandas as pd
import os
import json
import ast
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import json

load_dotenv()

router = APIRouter()

@router.get('/Reddit')
async def get_reddit_data():
    """ Returns all reddit data from database"""
    db_url = os.getenv('DB_URL')
    conn = psycopg2.connect(db_url)
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # if date_added == None:
    Q = """SELECT * FROM police_force;"""
    # else:
        # Q = f"""SELECT * FROM police_force WHERE added_on >= '{date_added}';"""
    curs.execute(Q)
    results = curs.fetchall()
    curs.close()
    conn.close()
    # print(type(results))
    # print(results)
    # df = pd.DataFrame(results)
    # df = df.fillna('None')
    # print(df.describe())
    # df.to_json()
    return results
    # return df.head().to_dict(orient='records')
    # return json.dumps(results, default=str)
    # return df.to_json(orient='records')
    # # return results

    # """
    # Convert data to usable json format
    # ### Response
    # dateframe: JSON object
    # """
    # for item in results:
    #     item['links'] = literal_eval(item['links'])
    #     item['tags'] = literal_eval(item['tags'])
    # return results