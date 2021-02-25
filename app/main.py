from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
import uvicorn
import pandas as pd
import psycopg2
import psycopg2.extras
import requests
import os
from dotenv import load_dotenv
from app import db, messages, twitter, reddit
from app.helper_funcs import check_new_items, preprocessNewData, getValues
from app.helper_vars import pb2020_insert_query, API_URL

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

@app.on_event('startup')
@repeat_every(seconds=60*60*24)  # runs function below every 24 hours 
async def run_update() -> None:

    # get all incidents stored in database
    DB_CONN = os.getenv('DB_URL')
    pg_conn = psycopg2.connect(DB_CONN) 
    pg_curs = pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    Q = """SELECT * FROM police_force;"""
    pg_curs.execute(Q)
    results = pg_curs.fetchall()
    pg_curs.close()

    # get all incidents on API
    r = requests.get(API_URL)
    data_info = r.json()
        
    #Checks for new incidents
    new_items = check_new_items(results,data_info) 

    # if there are new incidents, add them to database
    if new_items:
        newdata = preprocessNewData(new_items[:50])
        
        pg_conn = psycopg2.connect(DB_CONN)
        pg_curs = pg_conn.cursor()
        for item in newdata:
            pg_curs.execute(pb2020_insert_query, getValues(item))
        pg_conn.commit()
        pg_curs.close()
        pg_conn.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)