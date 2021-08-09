import requests
import os
import json
from typing import List, Dict
import tweepy
from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv
from scrap_paper import quick_reply_use_of_force

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"),
                           os.getenv("CONSUMER_SECRET"))
auth.set_access_token(os.getenv("ACCESS_KEY"), os.getenv("ACCESS_SECRET"))
api = tweepy.API(auth, wait_on_rate_limit=True)

manual_twitter_auth = OAuth1Session(os.getenv("CONSUMER_KEY"),
                                    os.getenv("CONSUMER_SECRET"),
                                    os.getenv("ACCESS_KEY"), os.getenv("ACCESS_SECRET"))

# Just my own for now
blue_witness_recipient_id = 271825982

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
                }
            },
            'source_app_id': '21602950',
            'name': 'new name'
        },
        'apps': {
            '21602950': {
                'id': '21602950',
                'name': 'bluewitness1'
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


list_of_quick_replies = [quick_reply_use_of_force]


def create_welcome_message(name: str, msg_txt: str, quick_replies: List[Dict] = None) -> Dict:

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

    welcome_response = json.loads(response.text)
    list_of_welcome_messages.append(welcome_response)


def reply_to_tweet(tweet_id, reply_text, welcome_message_name, blue_witness_recipient_id):
    for welcome_message in list_of_welcome_messages:
        if welcome_message['name'] == welcome_message_name:
            welcome_message_id = welcome_message['welcome_message']['id']
    dm_link = f'https://twitter.com/messages/compose?recipient_id={blue_witness_recipient_id}&welcome_message_id={welcome_message_id}'
    reply_message = f"{reply_text} \n {dm_link}"
    api.update_status(reply_message, in_reply_to_status_id=tweet_id)
