""" This Module Holds the Fast API to Launch the DS APP and API Calls"""

from app.db import ForceRanks, ScriptMaster
from random import choice
from typing import Dict, List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from pydantic import BaseModel

from app.scraper import deduplicate, frankenbert_rank, scrape_twitter, DB
import app.bot as bot

description = """
DS API for the Human Rights First Blue Witness Dashboard

To use these interactive docs:
- Click on an endpoint below
- Click the **Try it out** button
- Edit the Request body or any parameters
- Click the **Execute** button
- Scroll down to see the Server response Code & Details
"""

script_master = ScriptMaster()  # Scripts for the bot to pick from


class InputString(BaseModel):
    """
    guarantees that the fields of the resultant model 
    instance will conform to the field types defined on the model.
    Documentation Here: https://pydantic-docs.helpmanual.io/usage/models/
    """
    text: str


app = FastAPI(
    title='Labs 37 HRF BW DS API',
    description=description,
    docs_url='/',
    version="0.37.1",
)

# FastAPI Models


class form_out(BaseModel):
    form: int
    incident_id: int
    link: str
    tweet_id: str
    user_name: str


class form_in(BaseModel):
    city: str
    state: str
    confidence: Optional[float] = 0
    description: str
    force_rank: str
    incident_date: str
    incident_id: int
    lat: Optional[float] = None
    long: Optional[float] = None
    src: List[str] = []
    status: str
    title: str
    tweet_id: str
    user_name: str


class check(BaseModel):
    tweet_id: str


class new_script(BaseModel):
	script_id: int
	script: str
	convo_node: int
	use_count: Optional[int] = 0
	positive_count: Optional[int] = 0
	success_rate: Optional[float] = 0.0
	active: Optional[bool] = True


@app.post("/form-out/", response_model=form_out)
async def create_form_out(data: form_out):
    """
    replies to a given tweet with a link,
    prompting a Twitter user to send a dm to our bot
    """
    DB.update_tables(
        {"status":"awaiting response"}, data.tweet_id, "ForceRanks")
    bot.send_form(data)


@app.post("/form-in/")
async def create_form_in(data: form_in):
    """ receives form response and stores in Conversations table """
    location = bot.find_location(data.city + ',' + data.state)
    if location['status'] == "OK":
        loc_list = location['candidates'][0]['formatted_address'].split(',')

        if len(loc_list) == 4:
            city = loc_list[1]
            state = loc_list[2].split()[0]

        if len(loc_list) == 3:
            city = loc_list[0]
            state = loc_list[1].split()[0]

        data.lat = location['candidates'][0]['geometry']['location']['lat']
        data.long = location['candidates'][0]['geometry']['location']['lng']
    else:
        print(location['status'])
    bot.receive_form(data)


@app.post("/approval-check/")
async def create_check(data: check):
    """ returns value of Conversations table row with given tweet_id """
    out = DB.get_root_twelve(data.tweet_id)
    return out


@app.post("/approve/")
async def approve(data: check):
    """ updates ForceRanks with value of Conversations table row which is a form response """
    for_update = DB.get_root_twelve(data.tweet_id)
    data = {}
    data['city'] = for_update[0]['Conversations'].root_tweet_city
    data['state'] = for_update[0]['Conversations'].root_tweet_state
    data['force_rank'] = for_update[0]['Conversations'].root_tweet_force_rank
    data['incident_date'] = for_update[0]['Conversations'].root_tweet_date
    data['status'] = 'approved'
    data['lat'] = for_update[0]['Conversations'].root_tweet_lat
    data['long'] = for_update[0]['Conversations'].root_tweet_long

    DB.update_tables(data, for_update[0]['Conversations'].tweet_id, "ForceRanks")
    data2 = {}
    data2['conversation_status'] = 13
    DB.update_tables(data2, for_update[0]['Conversations'].tweet_id, "Conversations")
    return data


@app.post("/add-script/", response_model=new_script)
async def post_script(data: new_script):
    """
    This endpoint allows the Admin to put a new script into the bot_scripts
    table. If the conversation node for this script is "welcome" then either
    the capability to authorize a welcome message with twitter needs to be
    implemented or the Administrator needs to have the option to input the ID
    given by Twitter when authorizing a welcome script for the Blue Witness
    Twitter Account outside of this API

    https://whimsical.com/script-selection-2xBPsVkfFyfdjMTPQVUHfQ
    """
    script_master.add_script(data)


@app.post("/deactivate-script/")
async def deactivate(script_id):
    """
    Endpoint for the front end to utilize in the toggle funtion on the
    Script Management modal see:

    https://whimsical.com/script-selection-2xBPsVkfFyfdjMTPQVUHfQ
    """
    script_master.deactivate_script(script_id)


@app.post("/activate-script/")
async def activate(script_id):
    """
    Endpoint for the front end to utilize in the toggle funtion on the
    Script Management modal see:

    https://whimsical.com/script-selection-2xBPsVkfFyfdjMTPQVUHfQ
    """
    script_master.activate_script(script_id)


# Testing endpoint
@app.post("/bump-use-count/")
async def add_one_to_use_count(script_id):
    """
    This is a testing endpoint used to ensure that the functions for
    incrementing use counts in the 'bot_scripts' table work properly. No one 
    will need to grab these endpoints for anything else. The scriptmaster
    function called below will actually be called as a helper function within
    bot.py when the Twitter bot has selected a script for use and sent a
    tweet out.
    """
    script_master.add_to_use_count(script_id)


# Testing endpoint
@app.post("/update-pos-count/")
async def bump_pos_and_success_rate(script_id):
    """
    This is a testing endpoint used to ensure that the functions for
    incrementing positive counts in the 'bot_scripts' table work properly. No
    one will need to grab these endpoints for anything else. The scriptmaster
    function called below will actually be called as a helper function within
    bot.py when the Twitter bot has received feedback from a Twitter user and
    use this to bump the positve_count for the last script used.
    """
    script_master.add_to_positive_count(script_id)


@app.get("/select-all-from-bot-scripts/")
async def get_all_from_bot_scripts():
    """
    Selects all from 'bot_scripts' table to populate Script Management modal.
    """
    return DB.get_all_script_data()


@app.get("/frankenbert/{user_input}")
async def frankenbert(user_input: str):
    """ Prediction endpoint, for testing and demonstration purposes """
    rank, conf, *_ = frankenbert_rank(user_input)
    return {"Rank": rank, "Confidence": conf}


@app.get("/view-data/")
async def view_data():
    """ update and get first 5000 observations dump endpoint """
    await update()

    first_5000 = DB.get_table(ForceRanks)[:5000]
    return first_5000


@app.get("/to-approve/")
async def to_approve():
    """ get all rows of Conversations that are form responses that have not been approved """
    needs_approval = DB.get_twelves()
    return needs_approval


@repeat_every(seconds=60 * 60)
@app.get("/advance-all/")
async def advance_all():
    """ advances all conversations, repeats every hour, only one worker at a time """
    bot.advance_all()


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 4)
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
        'police abuse',
        'beaten', 'killed by police', 
        'taser', 'baton', 'use of force',
        'shot', 'lethal', 'non-lethal', 
        'pepper spray', 'oc', 'tear gas', 
        'rubber bullets', 'push', 
        'non-violent', 'tased', 'clashed with police',
        '#policebrutality', '#pig', '#pigs', 
        '#5-0', '#policeofficer', '#ACAB', 
        '#1312', '#fuckthepolice', 
        '#BlackLivesMatter', '#policeaccountability'
    ))
    data: List[Dict] = scrape_twitter(search)
    clean_data: List[Dict] = deduplicate(data)

    DB.insert_data_force_ranks(clean_data)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # List of approved origins
    allow_credentials=True,  # Can only allow certain headers as well
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    import uvicorn

    """ To run locally, use this command in the terminal:
    python3 -m app.main
    """
    uvicorn.run(app)
