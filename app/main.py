from random import choice
from typing import List, Dict, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from pydantic import BaseModel

from app.scraper import deduplicate, frankenbert_rank, scrape_twitter, DB
import app.bot as bot # This might work
# SHOULD LIMIT TO ONE DB IMPORT, WHAT MAKES THE MOST SENSE???

description = """
DS API for the Human Rights First Blue Witness Dashboard

To use these interactive docs:
- Click on an endpoint below
- Click the **Try it out** button
- Edit the Request body or any parameters
- Click the **Execute** button
- Scroll down to see the Server response Code & Details
"""

### MOVE TO MODELS

class form_out(BaseModel):
    form: int
    incident_id: int
    isChecked: bool
    link: str
    tweet_id: str
    user_name: str


class form_in(BaseModel):
    city: str
    confidence: Optional[float] = None
    description: str
    force_rank: str
    incident_date: str
    incident_id: int
    lat: float
    long: float
    src: List[str]
    state: str
    status: str
    title: str
    tweet_id: str
    user_name: str


class check(BaseModel):
    tweet_id: str

### MOVE TO MODELS


app = FastAPI(
    title='Labs 36 HRF BW DS API',
    description=description,
    docs_url='/',
    version="0.36.6",
)


@app.post("/form_in/")
async def create_form_in(data: form_in):
    return form_in
    # bot.send_form(form_in)


@app.post("/form_out/")
async def create_form_out(data: form_out):
    return form_out
    # bot.receive_form(form_out)


@app.post("/approval_check/")
async def create_check(data: check):
    return check
    # bot.DB


@app.get("/frankenbert/{user_input}")
async def frankenbert(user_input: str):
    """ Prediction endpoint, for testing and demonstration purposes """
    rank, conf, *_ = frankenbert_rank(user_input)
    return {"Rank": rank, "Confidence": conf}


@app.get("/view-data/")
async def view_data():
    """ update and get first 5000 observations dump endpoint """
    await update()

    first_5000 = DB.load_data_force_ranks()[:5000]
    return first_5000
    

@app.on_event("startup")
@repeat_every(seconds=60*60*4)
async def update():
    """ 1. scrape twitter for police use of force
        2. deduplicate data based on tweet id
        3. insert data into database
        4. repeat every 4 hours """
    search = choice((
        'police', 'pigs',
        'cops', 'ACAB', 'arrested',
        'police brutality',
        'police violence',
        'police abuse'
    ))
    data: List[Dict] = scrape_twitter(search)
    clean_data: List[Dict] = deduplicate(data)

    DB.insert_data_force_ranks(clean_data)



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
