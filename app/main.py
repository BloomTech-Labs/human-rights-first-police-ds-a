### This file is not being used for now but is kept as reference
### or in case it is necessary to implement in the future

import requests
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from app import db, twitter, reddit
from app.scraper import update_twitter_data
from app.helper_funcs import check_new_items, preprocess_new_data, load_data, insert_data
from app.create_db_tables import initialize_police_table

import logging
# create log to track when scraper is called
logging.basicConfig(filename='scraper.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO)
    


description = """
DS API for the Human Rights First Blue Witness Dashboard

To use these interactive docs:
- Click on an endpoint below
- Click the **Try it out** button
- Edit the Request body or any parameters
- Click the **Execute** button
- Scroll down to see the Server response Code & Details
"""

app = FastAPI(
    title='Labs 36 HRF BW DS API',
    description=description,
    docs_url='/',
)

app.include_router(db.router, tags=['Database'])
app.include_router(reddit.router, tags=['Reddit'])
app.include_router(twitter.router, tags=['Twitter'])


# # Uncomment if new tables need to be generated
# initialize_police_table()
# print('CREATED NEW TABLE')


@app.on_event('startup')
@repeat_every(seconds=60*60)  # set to run function below every 24 hours 60*60*24
async def run_update() -> None:
    # get all reddit incidents stored in database
    results = load_data()
    # get all incidents on PB2020 API
    pb2020_api_url = 'https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations-v2.json'
    r = requests.get(pb2020_api_url)
    data_info = r.json()
    #Checks for new incidents from PB2020
    new_items = check_new_items(results, data_info)
    # if there are new PB2020 incidents, add them to database
    if new_items:
        new_data = preprocess_new_data(new_items[:350])
        # insert data into police_force table
        insert_data(new_data)
    #get all reddit incidents, updated
    new_results = load_data()
    #Add to scraper.log when scraper is called
    logging.info('is when the scraper was called')
    #updates possible incidents from twitter
    update_twitter_data()
    # Add to scraper log when scraper has finished
    logging.info('is when the scraper finished')

    


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
