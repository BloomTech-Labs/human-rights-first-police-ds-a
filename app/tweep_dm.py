""" The purpose of this module is to set up tweepy for dms"""

import json
import os
import re
from typing import Dict, List

import requests
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


# witt_rowen welcome message = 1424836133582774286


# This will change and instead pull the welcome messages from twitter but for now storing locally for ease of use
list_of_welcome_messages = [
    {
        'welcome_message': {
            'id': '1424836133582774286',
            'created_timestamp': '1628542381078',
            'message_data': {
                'text': 'new message',
                'entities': {
                    'hashtags': [],
                    'symbols': [],
                    'user_mentions': [],
                    'urls': []
                },
                "quick_reply": {
                    "type": "options",
                    "options": [
                        {
                            "label": "Yes",
                            "metadata": "Yes",
                            #"description": "Yes"
                        },
                        {
                            "label": "No",
                            "metadata": "No",
                            #"description": "Open Handed (Arm Holds & Pushing)"
                        }
                    ]
                }
            },
            'source_app_id': '1335727237400694784',
            'name': 'new name'
        },
        'apps': {
            '21602950': {
                #'id': '21602950',
                'id': '1335727237400694784',
                'name': 'RowenWitt'
            }
        }
    },
    {
        'welcome_message': {
            "id": "1424835217869709320",
            "created_timestamp": "1628542162755",
            "message_data": {
                "text": "new message",
                "entities": {
                    "hashtags": [],
                    "symbols": [],
                    "user_mentions": [],
                    "urls": []
                },
                "quick_reply": {
                    "type": "options",
                    "options": [
                        {
                            "label": "Rank 1",
                            "metadata": "force_rank_1",
                            "description": "Non-violent Police Presence."
                        },
                        {
                            "label": "Rank 2",
                            "metadata": "force_rank_2",
                            "description": "Open Handed (Arm Holds & Pushing)"
                        },
                        {
                            "label": "Rank 3",
                            "metadata": "force_rank_3",
                            "description": "Blunt Force Trauma (Batons & Shields)"
                        },
                        {
                            "label": "Rank 4",
                            "metadata": "force_rank_4",
                            "description": "Chemical & Electric Weapons (Tasers & Pepper Spray)"
                        },
                        {
                            "label": "Rank 5",
                            "metadata": "force_rank_5",
                            "description": "Lethal Force (Guns & Explosives)"
                        }
                    ]
                }
            }
        }
    }
]
# Change to dict with keys of date location, and confirmation. Values list of A/B text
list_of_A_B_txts = [
    'Hi! I am a bot for Blue Witness, a project by @humanrights1st. We noticed your tweet may involve police misconduct, please confirm the date of this incident here: ',
    'Hi! I am a bot for Blue Witness, a project by @humanrights1st. We noticed your tweet may involve police misconduct, please confirm the location of this incident here: ',
]


def get_tweet_id(tweet_url):
    """Get the tweet ID from the tweet URL"""
    tweet_id = re.search(r'\d+$', tweet_url)
    return tweet_id.group(0)


def form_tweet(tweet_source: str, information_requested: str) -> Dict:
    tweet_id = get_tweet_id(tweet_source)
    if information_requested == 'date':
        tweet_txt = list_of_A_B_txts[0]
    if information_requested == 'location':
        tweet_txt = list_of_A_B_txts[1]
    link = os.getenv("FORM_URL")
    reply_message = f"{tweet_txt} \n {link}"
    tweet = api.update_status(reply_message, in_reply_to_status_id=tweet_id,
                              auto_populate_reply_metadata=True)
    return tweet


def create_welcome_message(name: str,
                           msg_txt: str,
                           quick_replies: List[Dict] = None):

    url = "https://api.twitter.com/1.1/direct_messages/welcome_messages/new.json"
    if quick_replies:
        payload = json.dumps({
            "welcome_message": {
                "name": name,
                "message_data": {
                    "text": msg_txt,
                    "quick_reply": {
                        "type": "options",
                        "options": quick_replies
                    }
                }
            }
        })
    else:
        payload = json.dumps({
            "welcome_message": {
                "name": name,
                "message_data": {
                    "text": msg_txt
                }
            }
        })
    headers = {
        'Content-Type': 'application/json'
    }

    response = manual_twitter_auth.post(url, headers=headers, data=payload)
    print(response)
    welcome_response = json.loads(response.text)
    list_of_welcome_messages.append(welcome_response)
    return list_of_welcome_messages


# Can take out for loop for welcome_message by just using welcome_message_id
# Have the welcome_message_name be displayed to admin but have it pass welcome_message_id


def reply_to_tweet(tweet_id,
                   reply_text,
                   welcome_message_name,
                   blue_witness_recipient_id):
    """Build the inital response tweet that will be used to reply to the user's incident tweet"""
    for welcome_message in list_of_welcome_messages:
        if welcome_message['name'] == welcome_message_name:
            welcome_message_id = welcome_message['welcome_message']['id']
    dm_link = f'https://twitter.com/messages/compose?recipient_id={blue_witness_recipient_id}&welcome_message_id={welcome_message_id}'
    reply_message = f"{reply_text} \n {dm_link}"
    api.update_status(reply_message, in_reply_to_status_id=tweet_id,
                      auto_populate_reply_metadata=True)


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
                "quick_reply_response": dm.message_create['message_data']['quick_reply_response']['metadata']
            })
    # have this just commit to db
    return dm_list


def send_clarification_dm(dm_id, A_B_txt, quick_replies: List[Dict] = None, ):
    """ Sends DM to twitter user_id with quick reply options to clarify if tweet is police misconduct. """
    user_id = None  # Use dm_id to search db for recipient_id

    api.send_direct_message(user_id, A_B_txt, quick_replies)


def get_response_dms(dm_id_list: List[Dict]) -> List[Dict]:
    """ Function to get DMs after initial response """
    # Need to get a list of dm_ids from database to then check for responses

    pass
