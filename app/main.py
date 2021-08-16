from random import choice
from typing import List, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from app.db import insert_data, load_data
from app.scraper import deduplicate, frankenbert_rank, scrape_twitter
from app.models import RequestedFormData
from app.tweep_dm import form_tweet


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
    title='Labs 37 HRF BW DS API',
    description=description,
    docs_url='/',
    version="0.37.1",
)


@app.post("/form/send")
async def send_form_tweet(data: RequestedFormData):
    '''
    Sends a reply tweet with a linked form to gather additional information on an incident.

    Args:
        data (RequestedFormData):  JSON containing information required to send reply tweet with form link
            data.tweet_source (str): Full URL to source tweet
            data.information_requested (str): One of a pre-defined set of information requests

    Returns:
        tweet.id (int): ID of the tweet that was sent
    '''
    tweet = form_tweet(data.tweet_source, data.information_requested)
    return tweet.id


@app.get("/frankenbert/{user_input}")
async def frankenbert(user_input: str):
    """ Prediction endpoint, for testing and demonstration purposes """
    rank, conf, *_ = frankenbert_rank(user_input)
    return {"Rank": rank, "Confidence": conf}


@app.get("/view-data/")
async def view_data():
    await update()
    return load_data()


@app.on_event("startup")
@repeat_every(seconds=60*60*4)
async def update():
    """ 1. scrape twitter for police use of force
        2. deduplicate data based on tweet id
        3. insert data into database
        4. repeat every 4 hours """
    search = choice((
        'police',
        'police brutality',
        'police violence',
        'police abuse',
    ))
    data: List[Dict] = scrape_twitter(search)
    clean_data: List[Dict] = deduplicate(data)
    insert_data(clean_data)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    import uvicorn
    """ To run locally, use this command in the terminal:
    python3 -m app.main
    """
    uvicorn.run(app)
