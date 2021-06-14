import tweepy
import pandas as pd

CONSUMER_KEY = "LU6eEdt9a4PwQWIqnJtyVnIp9"
CONSUMER_SECRET = "jTCDms0tUgq91AQXXHKSzsuLorSSpSCPb4TTWOxfurrmk6q3gm"
ACCESS_KEY = "1372271424241602564-xIh4fpuVRXwrllCDSYdZyH8vDutziy"
ACCESS_SECRET = "OM6t5cBI5yOCVJd9uG3sFFmBmFpHQgvV2LWVP9mKkQDvN"


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
try:
    api.verify_credentials()
    print('Authorized')
except:
    print('Error during authentication')


def get_mentions():
    for response in api.mentions_timeline():
        print(response.id_str)


def twitter_reply(reply_id, username, text):
    if text == "":
        reply_text = '''
        ------- test -------
        We noticed that you are reporting a police incident.
        '''
    else:
        reply_text = text

    tweet = api.update_status(status = f"@{username}: {reply_text}", in_reply_to_status_id=reply_id,tweet_mode = 'extended')
    return tweet


def direct_message(username):
    user = api.get_user(username)
    message = '''
    Just testing some features.
    This sends a direct message to the person
    '''
    api.send_direct_message(user.id, message)
    return 'direct message sent'

