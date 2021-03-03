from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
import uvicorn
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from app import db, twitter, reddit
from app.helper_funcs import check_new_items, preprocessNewData, getValues
from app.scraper import update_twitter_data 
from app.helper_funcs import check_new_items, preprocessNewData, loadData, insertData


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
app.include_router(reddit.router, tags= ['Reddit'])
app.include_router(twitter.router, tags=['Twitter'])

@app.on_event('startup')
@repeat_every(seconds=60*60*12)  # runs function below every 24 hours 
async def run_update() -> None:
    #updates possible incidents from twitter
    update_twitter_data()

    # get all reddit incidents stored in database
    results = loadData()
    
    # get all incidents on pb2020 API
    PB2020_API_URL = 'https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations-v2.json'
    r = requests.get(PB2020_API_URL)
    data_info = r.json()
        
    #Checks for new incidents from PB2020
    new_items = check_new_items(results,data_info) 

    # if there are new PB2020 incidents, add them to database
    if new_items:
        newdata = preprocessNewData(new_items[:350])
        
        # insert data into police_force table
        insertData(newdata)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)