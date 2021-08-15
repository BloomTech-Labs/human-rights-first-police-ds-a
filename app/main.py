from random import choice
from typing import List, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every


from app.scraper import deduplicate, frankenbert_rank, scrape_twitter, DB
import app.bot as bot
from app.models import form_out, form_in, check


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
    version="0.36.6",
)


@app.post("/form-out/", response_model=form_out)
async def create_form_out(data: form_out):
    """ replies to a given tweet with a link """
    DB.update_force_rank({"status":"awaiting response"}, data.tweet_id)
    bot.send_form(data)



@app.post("/form-in/")
async def create_form_in(data: form_in):
    """ receives form response and stores in holding table """
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
    """ returns value of holding table row with given tweet_id """
    out = DB.get_root_seven(data.tweet_id)
    return out


@app.post("/approve/")
async def approve(data: check):
    """ updates force_ranks with value of holding table row which is a form response """
    for_update = DB.get_root_seven(data.tweet_id)
    data = {}
    data['city'] = for_update[0]['Conversations'].root_tweet_city
    data['state'] = for_update[0]['Conversations'].root_tweet_state
    data['force_rank'] = for_update[0]['Conversations'].root_tweet_force_rank
    data['incident_date'] = for_update[0]['Conversations'].root_tweet_date
    data['status'] = 'approved'
    data['lat'] = for_update[0]['Conversations'].root_tweet_lat
    data['long'] = for_update[0]['Conversations'].root_tweet_long

    DB.update_force_rank(data, for_update[0]['Conversations'].root_tweet_id)
    return data


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
