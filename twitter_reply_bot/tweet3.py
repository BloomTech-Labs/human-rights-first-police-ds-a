from dotenv import load_dotenv, find_dotenv

import requests, time, json, re
import tweepy
import os
import logging
from typing import Tuple, List, Dict
import psycopg2
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, insert, update, func
from sqlalchemy.orm import sessionmaker
load_dotenv()
#load_dotenv(find_dotenv())

###### TODO #####
### DB DE-IDIOTIZATION ###
# Make global engine, use scoped sessions
# Switch over all psycopg2 code to sqlalchemy
# remove all print statements


### CORE FUNCTIONALITY ###
# create model for yes/no extraction
# swap out hardcoded input names for variables
# figure out approach for multiple responses to a given tweet from the user we're interested in
# finish setting up error logging
# setup external error logging server

### A/B TESTING ###
# build stats checker for A/B testing, stale conversations by reachout template/conversation step
# put test info in one place
# add table column for form/bot boolean

### TESTING, DOCS & CONSISTENCY ###
# put all functions in two classes
# make all variable names and function descriptors follow same format
# write good docstrings
# write unit tests
##### ##### ##### #####

#---------------------------------------------------------------------------------------#
# search words are 'police', 'police brutality', 'police violence', ' police abuse'
# test 1 tweetId = 1423359730983051266
# witt_rowen thread test root 1423714816145772545
# f = tweet2.get_replies('RowenWitt', '1423359730983051266', 'witt_rowen') # to get tweets
# witt_rowen - userid: 1078337070, tweetid: 1423359730983051266
#---------------------------------------------------------------------------------------#

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

db2 = os.getenv("DB2")

#engine = create_engine(db2, pool_recycle=3600, echo=False)
engine = create_engine(db2)
metadata = MetaData(engine)
# Session = scoped_session(sessionmaker())
# Session.configure(bind=engine)


conversations = Table(
		'conversations', metadata,
		Column('id', Integer, primary_key = True),
		Column('root_tweet_id', String),  # Should be able to relate to main DB, if status == 5, push to main db
		Column('sent_tweet_id', String),
		Column('received_tweet_id', String), #Could be combined with above?
		Column('in_reply_to_id', String),
		Column('tweeter_id', String),  # screen_name
		Column('conversation_status', Integer), # query to get largest of each conv_id
		Column('tweet_text', String),  # just to have the text for records
		Column('checks_made',Integer),  # iterate each time check is made
		Column('reachout_template', String)
	)
# full_conversations_insert = [{"root_tweet_id":"","sent_tweet_id":"","recieved_tweet_id":"",}]

bot_name = 'RowenWitt'

conversation_tree = {
	1:"Hi, do you have more information about the location of this incident?",
	2:"What is the location where this incident took place?",
	3:"Thanks! You're helping (align incentives)!",
	4:"Thanks anyway!"
}

test_entries = [
	{"root_tweet_id":"1424511565932359685","tweeter_id":"witt_rowen","conversation_status":0,"tweet_text":"Incident report test 1 🦟📡","checks_made":0},
	{"root_tweet_id":"1424420702208237573","tweeter_id":"witt_rowen","conversation_status":0,"tweet_text":"Incident report test 2 🐥","checks_made":0},
	{"root_tweet_id":"1424452159744077826","tweeter_id":"witt_rowen","conversation_status":0,"tweet_text":"Incident report test 3🦧","checks_made":0},
	#{"root_tweet_id":"1424591950544478212","tweeter_id":"SckPpptBW","conversation_status":0,"tweet_text":"Incident report test 1 🕵️\u200d♂️","checks_made":0}
]

demo_entries = [
	{"root_tweet_id":"1424591950544478212","tweeter_id":"SckPpptBW","conversation_status":0,"tweet_text":"Incident report test 1 🕵️\u200d♂️","checks_made":0}
	]


def create_api():
	consumer_key = os.getenv("TWITTER_API_KEY")
	consumer_secret = os.getenv("TWITTER_API_KEY_SECRET")
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
		print('failed')
		raise e
	logger.info("API created")
	return api

api = create_api()

def create_conversations_table():
	#session = Session()
	#conversations.create(engine)
	meta = MetaData()
	conversations = Table(
		'conversations', meta,
		Column('id', Integer, primary_key = True),
		Column('root_tweet_id', String),  # Should be able to relate to main DB, if status == 5, push to main db
		Column('sent_tweet_id', String),
		Column('received_tweet_id', String), #Could be combined with above?
		Column('in_reply_to_id', String),
		Column('tweeter_id', String),  # screen_name
		# Column('conversation_id', Integer),
		Column('conversation_status', Integer), # query to get largest of each conv_id
		Column('tweet_text', String),  # just to have the text for records
		Column('checks_made',Integer),  # iterate each time check is made
		Column('reachout_template', String)
	)
	metadata.create_all(engine)

def drop_conversations_table():
	# engine = create_engine(db2)
	# meta = MetaData()
	conversations = Table(
		'conversations', metadata,
		Column('id', Integer, primary_key = True),
		Column('root_tweet_id', String),  # Should be able to relate to main DB, if status == 5, push to main db
		Column('sent_tweet_id', String),
		Column('received_tweet_id', String), #Could be combined with above?
		Column('in_reply_to_id', String),
		Column('tweeter_id', String),  # screen_name
		# Column('conversation_id', Integer),
		Column('conversation_status', Integer), # query to get largest of each conv_id
		Column('tweet_text', String),  # just to have the text for records
		Column('checks_made',Integer),  # iterate each time check is made
		Column('reachout_template', String)
	)
	conversations.drop(engine)

def load_data_conversations() -> List[Tuple]:
	"""Get all data from conversations"""
	with engine.begin() as connection:
		query = select(conversations)
		conversations_data = connection.execute(query)
	return conversations_data.fetchall()

def get_conversation_root(root_id: int) -> List[Tuple]:
	"""Get conversations with a specific root"""
	with engine.begin() as connection:
		query = select(conversations).where(conversations.c.root_tweet_id == root_id)
		conversations_data = connection.execute(query)
	return conversations_data.fetchall()

def load_data_force_rank() -> List[Tuple]:
	"""Get all data from force_rank"""
	select_query = "SELECT * FROM force_ranks"
	conn = psycopg2.connect(db2)
	curs = conn.cursor()
	curs.execute(select_query)
	data = curs.fetchall()
	curs.close()
	conn.close()
	return data

def get_no_location_force_rank() -> List[Tuple]:
	"""Get all rows where location is pending"""
	# null_loc = 'SELECT * FROM force_ranks WHERE city is Null or state is Null'
	test_loc = "SELECT * FROM force_ranks WHERE force_rank LIKE '%Rank 0 - Test'"
	conn = psycopg2.connect(db2)
	curs = conn.cursor()
	curs.execute(test_loc)
	data = curs.fetchall()
	curs.close()
	conn.close()
	return data

def insert_conversations(data: List[dict]) -> str:  # wherever output is string on u func, log status
	# fmt [{"id":0,"root_tweet_id":'',"sent_tweet_id":'',"received_tweet_id":'',"in_reply_to_id":'',"conversation_status":0,"tweet_text":''}]
	# Need to check existing conversations against root_id, and increment conversation_id
	with engine.begin() as connection:
		for datum in data:
			ins = conversations.insert().values(datum)
			connection.execute(ins)

		### WRITE - do I need to write line by line? manage rollback?

# should switch over db interface to sqlalchemy, req'd for this user input table, should do both for consistency
def insert_force_rank(data: List[Tuple]) -> str: 
	insert_query = 'INSERT INTO force_ranks(incident_id, incident_date, tweet_id, user_name, description, city, state, lat, long, title, force_rank, status, confidence, tags, src) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
	conn = psycopg2.connect(db2)
	curs = conn.cursor()
	for datum in data:
		curs.execute(insert_query, datum)
		conn.commit()
	curs.close()
	conn.close()
	print("Wrote {} entries to db2".format(len(data)))

def update_force_rank_location(data: Tuple, tweet_id: int) -> str:
	update_query = 'UPDATE force_ranks SET city=%s, state=%s, lat=%s, long=%s WHERE tweet_id=%s'
	conn = psycopg2.connect(db2)
	curs = conn.cursor()
	curs.execute(update_query, (data['city'],data['state'],data['lat'],data['long'],tweet_id))
	conn.commit()
	curs.close()
	conn.close()
	print('Updated {}'.format(tweet_id))


def get_to_advance() -> List[Tuple]:
	# for each root_id, get highest conversation_status
	with engine.begin() as connection:
		query1 = select(func.max(conversations.c.conversation_status).label("status"), conversations.c.root_tweet_id).group_by(conversations.c.root_tweet_id).cte('wow')
		query2 = select(conversations).join(query1, query1.c.root_tweet_id==conversations.c.root_tweet_id).filter(conversations.c.conversation_status==query1.c.status)
		data = connection.execute(query2)
	return data

def advance_all():
	to_advance = get_to_advance()
	for points in to_advance:
		advance_conversation(points[1])
		print('success', points[1])



def clean_str(string: str) -> str:
	return string.replace('\n', ' ').replace("'", "’")

def scrape_twitter(query: str) -> List[Dict]:
	tweets = []
	for status in tweepy.Cursor(
		api.search,
		q=query,
		lang='en',
		tweet_mode="extended",
		count=100
	).items(500):
		tweets.append({
			"tweet_id": status.id_str,
			"user_name": clean_str(status.user.name),
			"description": clean_str(status.full_text),
			"src": f'["https://twitter.com/{status.user.screen_name}/status/{status.id_str}"]'
		})
	return tweets


def user_tweets(user_id: str) -> List[Dict]:
	"""For testing, getting one user's tweets for tweet ids to test reponse"""
	temp = api.user_timeline(screen_name=f'{user_id}',
		count = 200,
		include_rts = False,
		tweet_mode='extended')
	tweets = []
	for tweet in temp:
		tweets.append({
			"tweet_id":tweet.id,
			"full_text":tweet.full_text,
			"author":tweet.author.screen_name
			})
	return tweets

def respond_to_tweet(tweet_id: int, tweet_body: str) -> str:
	"""Function to reply to a certain tweet_id"""
	return api.update_status(status=tweet_body, in_reply_to_status_id = tweet_id, auto_populate_reply_metadata=True)

def reset_conversations_for_test():
	drop_conversations_table()
	create_conversations_table()
	insert_conversations(test_entries)
	print("done, you idiot")

def end_conversation(root_id: int, max_step: List):
	other_person = api.get_status(max_step[3])
	other_person = other_person.user.screen_name
	test = get_replies(bot_name, max_step[2], other_person) ## (me, last tweet I sent, person I'm talking to)
	if test:
		try:
			status = respond_to_tweet(test.id_str, conversation_tree[4])
			to_insert = [{"root_tweet_id":root_id,"sent_tweet_id":status.id,"received_tweet_id":test.id_str,"in_reply_to_id":test.in_reply_to_status_id,"tweeter_id":test.in_reply_to_screen_name,"conversation_status":5,"tweet_text":test.full_text,"checks_made":(max_step[8]+1),"reachout_template":conversation_tree[4]}]
			insert_conversations(to_insert)
		except tweepy.TweepError as e:
			logging.error("Tweepy error occured:{}".format(e))
	else:
		print('error here')

def update_conversation_checks(root_id: int, max_step: List):
	query = (
		update(conversations).
		where(conversations.c.root_tweet_id == root_id).
		values(checks_made = (max_step[8]+1))
		)
	engine = create_engine(db2)
	with engine.begin() as connection:
		connection.execute(query)


# MAX(conversation_status)WHERE root_tweet_id LIKE '%1423714816145772545'
# update conversations will go something like this ^ to increment conversation_status
def advance_conversation(root_id: int) -> str:
	root_conversation = get_conversation_root(root_id)
	max = -1
	print(root_conversation)
	for steps in root_conversation: # this only matters once I can get the most recent reply
		print(steps)
		if steps[6] > max:
			max = steps[6]
			max_step = steps
			print(max_step)
	if max_step[6] == 0:
		try:
			status = respond_to_tweet(max_step[1], conversation_tree[1])
			# Need to get columns from status object
			print(max_step[6])
			print(max_step[7])
			print(max_step[9])
			to_insert = [{"root_tweet_id":root_id,"sent_tweet_id":status.id_str,"in_reply_to_id":status.in_reply_to_status_id,"tweeter_id":max_step[5],"conversation_status":(max_step[6]+1),"tweet_text":max_step[7],"checks_made":(max_step[8]+1),"reachout_template":conversation_tree[1]}]

			print(to_insert)
			insert_conversations(to_insert)
		except tweepy.TweepError as e:
			logging.error("Tweepy error occured:{}".format(e))

	elif max_step[6] == 1:
		print('works so far')
		test = get_replies(bot_name, max_step[2], max_step[5])
		if test:
			if test.full_text == '@RowenWitt Yes':  ###### INSERT CLASSIFICATION MODEL HERE ####
				try:
					status = respond_to_tweet(test.id_str,conversation_tree[2])
					to_insert = [{"root_tweet_id":root_id,"sent_tweet_id":status.id,"received_tweet_id":test.id_str,"in_reply_to_id":test.in_reply_to_status_id,"tweeter_id":test.in_reply_to_screen_name,"conversation_status":(max_step[6]+1),"tweet_text":test.full_text,"checks_made":(max_step[8]+1),"reachout_template":conversation_tree[2]}]
					print(to_insert)
					insert_conversations(to_insert)
					return test
				except tweepy.TweepError as e:
					logging.error("Tweepy error occured:{}".format(e))
			elif test.full_text == '@RowenWitt No': ###### INSERT CLASSIFICATION MODEL HERE ###
				end_conversation(root_id, max_step)
			else:
				end_conversation(root_id, max_step)
		else:
			#end_conversation(root_id, max_step)
			pass
	elif max_step[6] == 2:
		print('shit, we got this far')
		print(max_step)
		api = create_api()
		other_person = api.get_status(max_step[3])
		other_person = other_person.user.screen_name
		#test = get_replies(bot_name, max_step[2], other_person)  # Setup flip flop for variable input
		test = get_replies(bot_name, max_step[2], other_person)
		print(test.full_text)
		if test is not None:
			if test.full_text: # Validation goes here
				location = find_location(test.full_text.lstrip("@" + bot_name + " "))
				print(location)
				if location['status'] == "OK":
					loc_list = location['candidates'][0]['formatted_address'].split(',')
					if len(loc_list) == 4:
						city = loc_list[1]
						state = loc_list[2].split()[0]
			
					if len(loc_list) == 3:
						city = loc_list[0]
						state = loc_list[1].split()[0]
				
					latitude = location['candidates'][0]['geometry']['location']['lat']
					longitude = location['candidates'][0]['geometry']['location']['lng']
					update_data = {"city":city,"state":state,"lat":latitude,"long":longitude}
					print('START HERE ------------------')
					print(update_data)
					update_force_rank_location(update_data, root_id)
					try:
						status = respond_to_tweet(test.id, conversation_tree[3])
						to_insert = [{"root_tweet_id":root_id,"sent_tweet_id":status.id,"received_tweet_id":test.id_str,"in_reply_to_id":test.in_reply_to_status_id,"tweeter_id":test.in_reply_to_screen_name,"conversation_status":5,"tweet_text":test.full_text,"checks_made":(max_step[8]+1),"reachout_template":conversation_tree[3]}]
						print('LOOK HERE --------------------')
						print(to_insert)
						insert_conversations(to_insert)
					except tweepy.TweepError as e:
						logging.error("Tweepy error occured:{}".format(e))
				elif location['status'] == "ZERO_RESULTS":
					pass
					return end_conversation(root_id, max_step)
		else:
			pass
	elif max_step[6] == 5:
		# function to update checks
		update_conversation_checks(root_id, max_step)
		print('conversation_finished')


def get_user_id(screen_name: str) -> List[Dict]:
	"""Get user ids"""
	name_id_pairs = []
	resp = api.lookup_users(screen_name=screen_name)
	for user in resp:
		name_id_pairs.append({
			"screen_name":user.screen_name,
			"user_id":user.id
			})
	return name_id_pairs

def get_replies(user_id: str, tweet_id: int, tweeter_id: str) -> str:
	""" System to get replies to a given tweet, tweeted by user, replied by replier """
	# if type(user_id) != str:
	# 	user_id = get_user_id(user_id)
	replies = tweepy.Cursor(api.search, q='to:{}'.format(user_id),
		since_id=tweet_id, tweet_mode='extended').items(100)
	list_replies = []
	#print(replies.next())
	#return replies
	while True:
		try:

			reply = replies.next()
			if not hasattr(reply, 'in_reply_to_status_id_str'):
				continue
			if reply.in_reply_to_status_id == int(tweet_id) and reply.user.screen_name == tweeter_id:
				return reply
		except tweepy.RateLimitError as e:
			logging.error("Twitter api rate limit reached".format(e))
			time.sleep(60)
		except tweepy.TweepError as e:
			logging.error("Tweepy error occured:{}".format(e))
			break
		except StopIteration:
			print('StopIteration')
			break
		except Exception as e:
			logger.error("Failed while fetching replies {}".format(e))
			break



def clean_query_string(string: str) -> str:
	string.replace(' ', '%20')
	string.replace(',', '')
	return string


def find_location(query_string: str) -> Dict:
	query_string = clean_query_string(query_string)
	query='https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=formatted_address,geometry,name,place_id&key={}'.format(query_string, os.getenv("MAP_API"))
	resp = requests.get(query)
	data = json.loads(resp.content)
	return data

##############

# witt_rowen - 1078337070, 1423359730983051266
def send_dm(user_id: str, dm_body: str) -> str:
	"""Function to send dm"""
	api = create_api()
	dm = api.send_direct_message(user_id, dm_body)


def get_dms(count:int) -> List[Dict]:
	"""Function to get 'number' dms"""
	api = create_api()
	dms = api.list_direct_messages()
	dm_list = []
	for dm in dms:
		dm_list.append({
			"dm_id":dm.id,
			"time_created":dm.created_timestamp,
			"recipient_id":dm.message_create['target']['recipient_id'],
			"sender_id":dm.message_create['sender_id'],
			"text":dm.message_create['message_data']['text'],
			"hashtags":dm.message_create['message_data']['entities']['hashtags'],
			"symbols":dm.message_create['message_data']['entities']['symbols'],
			"user_mentions":dm.message_create['message_data']['entities']['user_mentions'],
			"urls":dm.message_create['message_data']['entities']['urls'],
			})
	return dm_list

# while True:
# 	advance_all()
# 	time.sleep(30)

# # Brody code, need to manage responses and build out conversation tree
# def send_clarification_tweet(username: str) -> str:
#     """ Sends DM to twitter user_id with quick reply options to clarify if tweet is police misconduct. """
#     api = create_api()
#     user = api.get_user(username)
#     txt = 'Hi! I am a bot for Blue Witness, a project by the Human Rights First. We noticed a tweet that may involve police misconduct, can you confirm this?'
#     quick_replies = [
#         {
#             "label": "Yes this is!",
#             "description": "You can confirm police misconduct occured.",
#             "metadata": "yes"
#         },
#         {
#             "label": "No this is not.",
#             "description": "You can not confirm police misconduct occured",
#             "metadata": "no"
#         },
#     ]
#     api.send_direct_message(user.id, txt, quick_reply_options=quick_replies)

# with cte as (
# 	SELECT MAX(conversation_status) status, root_tweet_id id FROM public.conversations GROUP BY root_tweet_id
# )


# select conversations.* from conversations
# inner join cte on cte.id = conversations.root_tweet_id
# where conversations.conversation_status = cte.status


# pos or neg sentiment model
# if pos -> "What is the location at which this incident occured?"
	# Call google api on response
# if neg -> "No problem, thanks anyway"

