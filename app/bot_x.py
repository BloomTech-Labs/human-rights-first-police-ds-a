
""" Create a twitter bot that delivers a form or starts a conversation with a user"""
import os # Need this to find environment variables
import tweepy # for access to the tweepy api,
"""
Tweepy documentation: https://docs.tweepy.org/en/stable/
"""
from dotenv import load_dotenv, find_dotenv
"""
dotenv loads the configuration variables from our .env file
dotenv documentation: https://pypi.org/project/python-dotenv/
"""

load_dotenv(find_dotenv()) # loads enviromental variables from .env

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.getenv("DEV_CONSUMER_KEY"), 
                            os.getenv("DEV_CONSUMER_SECRET")
                            ) 

auth.set_access_token(os.getenv("DEV_ACCESS_KEY"), 
                        os.getenv("DEV_ACCESS_SECRET")
                        )

# Create API object
api = tweepy.API(auth)

# Create a tweet
api.update_status("This is another test")

#TODO Get the bot to find an incident in the database and respond to that user. 