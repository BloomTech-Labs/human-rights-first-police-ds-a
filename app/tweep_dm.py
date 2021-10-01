""" The purpose of this module is to set up tweepy for dms"""

import json
import os
import re
from typing import Dict, List

import tweepy
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"),
                           os.getenv("CONSUMER_SECRET"))
auth.set_access_token(os.getenv("ACCESS_KEY"), os.getenv("ACCESS_SECRET"))
api = tweepy.API(auth, wait_on_rate_limit=True)

manual_twitter_auth = OAuth1Session(os.getenv("CONSUMER_KEY"),
                                    os.getenv("CONSUMER_SECRET"),
                                    os.getenv("ACCESS_KEY"),
                                    os.getenv("ACCESS_SECRET"))


def get_initial_dms(user_id: List[str]) -> List[Dict]:
    """Function to get DMs sent from button in tweet"""
    dms = api.list_direct_messages()
    dm_list = []
    for dm in dms:
        if dm.message_create['sender_id'] in user_id:
            dm_list.append({
                "dm_id": dm.id,
                "time_created": dm.created_timestamp,
                "welcome_message": dm.initiated_via['welcome_message_id'],
                "sender_id": dm.message_create['sender_id'],
                "text": dm.message_create['message_data']['text'],
                "quick_reply_response":
                    dm.message_create['message_data']['quick_reply_response'][
                        'metadata']
            })
    # have this just commit to db
    return dm_list

