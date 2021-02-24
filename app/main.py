from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
import uvicorn
from app import db, messages, twitter, reddit
from .helper_funcs import check_new_items, preprocessNewData, getValues
# from helper_vars import stop, VERBALIZATION, EMPTY_HAND_HARD, EMPTY_HAND_SOFT, LESS_LETHAL_METHODS, LETHAL_FORCE, UNCATEGORIZED
import pandas as pd
# from pandas import Timestamp
# import datetime
import psycopg2
import psycopg2.extras
import requests
from .helper_vars import stop, pb2020_insert_query
import os
from dotenv import load_dotenv

load_dotenv() 

description = """
Database for Human Rights First Dashboard

To use these interactive docs:
- Click on an endpoint below
- Click the **Try it out** button
- Edit the Request body or any parameters
- Click the **Execute** button
- Scroll down to see the Server response Code & Details
"""

app = FastAPI(
    title='Labs 31 HRF API',
    description=description,
    docs_url='/',
)

app.include_router(db.router, tags=['Database'])
app.include_router(messages.router, tags=['Friendly messages'])
app.include_router(reddit.router, tags= ['Reddit'])
app.include_router(twitter.router, tags=['Twitter'])

counters = 0

@app.on_event('startup')
# @repeat_every(seconds=60*60*24)  # Runs Function below every 24 hours. 
async def run_update() -> None:
    # Counts number of updates.
    global counters 
    print('Update Number:', counters)
    counters += 1
    # DB Connection
    DB_CONN = os.getenv('DB_URL') # Gets URL from Enviroment Variable
    pg_conn = psycopg2.connect(DB_CONN) # Connects to DB
    pg_curs = pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    Q = """SELECT * FROM police_force;"""
    pg_curs.execute(Q)
    results = pg_curs.fetchall()
    pg_curs.close()

    API_CONN = os.getenv('API_URL')
    r = requests.get(API_CONN)
    data_info = r.json()
        
    #Updates to database
    counter_api,new_items = check_new_items(results,data_info) #Checks for new items
    print('Number of new Items',counter_api)
    print('New Items: ', len(new_items))
    print('counters', counters)

    # if new_items array is not empty. add data to database
    if new_items:
        newdata = preprocessNewData(new_items)
        
        pg_conn = psycopg2.connect(DB_CONN)
        pg_curs = pg_conn.cursor()
        iterations = 0
        for item in newdata:
            pg_curs.execute(pb2020_insert_query, getValues(item))
            iterations += 1
        print(iterations)
        pg_conn.commit()
        pg_curs.close()
        pg_conn.close()
        print('Update Completed')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)