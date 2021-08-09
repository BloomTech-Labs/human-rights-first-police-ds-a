import tweepy
import logging
import time
import os
from dotenv import load_dotenv

load_dotenv()

# auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"))
# auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))

# api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# try:
# 	api.verify_credentials()
# 	print('Auth ok')
# except:
# 	print("Error during authentication")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def create_api():
	consumer_key = os.getenv("TWITTER_API_KEY")
	consumer_secret = os.getenv("TWITTER_API_SECRET")
	access_token = os.getenv("ACCESS_TOKEN")
	access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True,
		wait_on_rate_limit_notify=True)

	try:
		api.verify_credentials()
	except Exception as e:
		logger.error("Error creating API", exc_info=True)
		print('t')
		raise e
	logger.info("API created")
	return api

def check_mentions(api, keywords, since_id):
	logger.info("Retrieving mentions")
	new_since_id = since_id
	for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
		new_since_id = max(tweet.id, new_since_id)
		if tweet.in_reply_to_status is not None:
			continue
		if any(keyword in tweet.text.lower() for keyword in keywords):
			logger.info(f"Answering to {tweet.user.name}")

			if not tweet.user.following:
				tweet.user.follow()

			api.update_status(
				status="Please reach us via DM",
				in_reply_to_status_id=tweet.id,
			)
	return new_since_id

def main():
	api = create_api()
	since_id = 1
	while True:
		since_id = check_mentions(api, ["help, support"], since_id)
		logger.info("Waiting...")
		time.sleep(60)

if __name__ == "__main__":
	main()