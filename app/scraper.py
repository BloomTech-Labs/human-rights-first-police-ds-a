import dataset
import json
import tweepy
from sqlalchemy.exc import ProgrammingError
from os import getenv
from dotenv import load_dotenv

from textmatcher import TextMatcher
from training_data import ranked_reports

load_dotenv()

db = dataset.connect(getenv("DB_URL"))

model = TextMatcher(ranked_reports)

#insert your credentials here
CONSUMER_KEY = getenv("CONSUMER_KEY")
CONSUMER_SECRET = getenv("CONSUMER_SECRET")
ACCESS_KEY = getenv("ACCESS_KEY")
ACCESS_SECRET = getenv("ACCESS_SECRET")

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        filter_words = ["police", "officer", "cop"]
        ranked_reports = ["Rank 2 - Empty-hand", "Rank 3 - Blunt Force", 
                        "Rank 4 - Chemical & Electric", "Rank 5 - Lethal Force"]
        category = model(status.text)
        conditions = (not 'RT @' in status.text) and \
                    any(word in status.text for word in filter_words) \
                    and (category in ranked_reports)
        if conditions:
            description = status.user.description
            loc = status.user.location
            text = status.text
            coords = status.coordinates
            geo = status.geo
            name = status.user.screen_name
            user_created = status.user.created_at
            id_str = status.id_str
            created = status.created_at
            source = status.user.url
            language = status.lang

            if geo is not None:
                geo = json.dumps(geo)

            if coords is not None:
                coords = json.dumps(coords)

            table = db["twitter_potential_incidents"]
            try:
                table.insert(dict(
                    user_description=description,
                    user_location=loc,
                    coordinates=coords,
                    text=text,
                    geo=geo,
                    user_name=name,
                    user_created=user_created,
                    id_str=id_str,
                    created=created,
                    source = source,
                    language = language,
                    category = category
                    ))
            except ProgrammingError as err:
                print(err)

    def on_error(self, status_code):
        if status_code == 420:
            #return False in on_data disconnects the stream
            return False

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["police", "cop", "officer"])

if __name__ == '__main__':
    pass