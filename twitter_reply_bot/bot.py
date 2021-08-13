
import requests, time, json, re
import os, logging
from typing import Tuple, List, Dict
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, insert, update, func

from db import Database
import twitter


load_dotenv(find_dotenv())

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

DB = Database()

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


def create_conversations_table():
	meta = MetaData()
	conversations = Table(
		'conversations', meta,
		Column('id', Integer, primary_key = True),
		Column('root_tweet_id', String),  # Should be able to relate to main DB, if status == 5, push to main db
		Column('sent_tweet_id', String),
		Column('received_tweet_id', String), #Could be combined with above?
		Column('in_reply_to_id', String),
		Column('tweeter_id', String),  # screen_name
		Column('conversation_status', Integer), # query to get largest of each conv_id
		Column('tweet_text', String),  # just to have the text for records
		Column('checks_made',Integer),  # iterate each time check is made
		Column('reachout_template', String),
		extend_existing=True,
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
		Column('reachout_template', String),
		extend_existing=True,
	)
	conversations.drop(engine)


def advance_all():
	to_advance = DB.get_to_advance()
	for points in to_advance:
		advance_conversation(points.root_tweet_id)
		print('success', points.root_tweet_id)



def reset_conversations_for_test():
	drop_conversations_table()
	create_conversations_table()
	DB.insert_conversations(test_entries)
	print("done, you idiot")

def end_conversation(root_id: int, max_step: List, received_tweet_id=None):
	print("\n", "\n", "\n", max_step.__dict__)

	if received_tweet_id:
		other_person = api.get_status(received_tweet_id)
	else:
		other_person = api.get_status(max_step.received_tweet_id)

	other_person = other_person.user.screen_name
	test = twitter.get_replies(bot_name, max_step.sent_tweet_id, other_person) ## (me, last tweet I sent, person I'm talking to)
	if test:
		try:
			status = twitter.respond_to_tweet(test.id_str, conversation_tree[4])
			to_insert = [{
				"root_tweet_id":root_id,
				"sent_tweet_id":status.id,
				"received_tweet_id":test.id_str,
				"in_reply_to_id":test.in_reply_to_status_id,
				"tweeter_id":test.in_reply_to_screen_name,
				"conversation_status":5,"tweet_text":test.full_text,
				"checks_made":(max_step.checks_made+1),
				"reachout_template":conversation_tree[4]
			}]
			DB.insert_conversations(to_insert)
		except tweepy.TweepError as e:
			logging.error("Tweepy error occured:{}".format(e))
	else:
		print('error here')

# MAX(conversation_status)WHERE root_tweet_id LIKE '%1423714816145772545'
# update conversations will go something like this ^ to increment conversation_status
def advance_conversation(root_id: int) -> str:
	root_conversation = DB.get_conversation_root(root_id)
	max = -1
	print([i.__dict__ for i in root_conversation])
	for steps in root_conversation: # this only matters once I can get the most recent reply
		print(steps.__dict__)
		if steps.conversation_status > max:
			max = steps.conversation_status
			max_step = steps
			print(max_step.__dict__)
	if max_step.conversation_status == 0:
		try:
			status = twitter.respond_to_tweet(max_step.root_tweet_id, conversation_tree[1])
			# Need to get columns from status object
			print(max_step.conversation_status)
			print(max_step.tweet_text)
			print(max_step.reachout_template)
			to_insert = [{
				"root_tweet_id":root_id,
				"sent_tweet_id":status.id_str,
				"in_reply_to_id":status.in_reply_to_status_id,
				"tweeter_id":max_step.tweeter_id,
				"conversation_status":(max_step.conversation_status+1),
				"tweet_text":max_step.tweet_text,
				"checks_made":(max_step.checks_made+1),
				"reachout_template":conversation_tree[1]
			}]

			print(to_insert)
			DB.insert_conversations(to_insert)
		except tweepy.TweepError as e:
			logging.error("Tweepy error occured:{}".format(e))

	elif max_step.conversation_status == 1:
		print('works so far')
		test = twitter.get_replies(bot_name, max_step.sent_tweet_id, max_step.tweeter_id)
		if test:
			if test.full_text == '@RowenWitt Yes':  ###### INSERT CLASSIFICATION MODEL HERE ####
				try:
					status = twitter.respond_to_tweet(test.id_str,conversation_tree[2])
					to_insert = [{
						"root_tweet_id":root_id,
						"sent_tweet_id":status.id,
						"received_tweet_id":test.id_str,
						"in_reply_to_id":test.in_reply_to_status_id,
						"tweeter_id":test.in_reply_to_screen_name,
						"conversation_status":(max_step.conversation_status+1),
						"tweet_text":test.full_text,
						"checks_made":(max_step.checks_made+1),
						"reachout_template":conversation_tree[2]
					}]
					print(to_insert)
					DB.insert_conversations(to_insert)
					return test
				except tweepy.TweepError as e:
					logging.error("Tweepy error occured:{}".format(e))
			elif test.full_text == '@RowenWitt No': ###### INSERT CLASSIFICATION MODEL HERE ###
				end_conversation(root_id, max_step, received_tweet_id=test.id_str)
			else:
				end_conversation(root_id, max_step, received_tweet_id=test.id_str)
		else:
			#end_conversation(root_id, max_step)
			pass
	elif max_step.conversation_status == 2:
		print('shit, we got this far')
		print(max_step)
		api = create_api()
		other_person = api.get_status(max_step.received_tweet_id)
		other_person = other_person.user.screen_name
		#test = get_replies(bot_name, max_step[2], other_person)  # Setup flip flop for variable input
		test = twitter.get_replies(bot_name, max_step.sent_tweet_id, other_person)

		if test is not None:
			print(test.full_text)
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
					DB.update_force_rank_location(update_data, root_id)
					try:
						status = twitter.respond_to_tweet(test.id, conversation_tree[3])
						to_insert = [{
							"root_tweet_id":root_id,
							"sent_tweet_id":status.id,
							"received_tweet_id":test.id_str,
							"in_reply_to_id":test.in_reply_to_status_id,
							"tweeter_id":test.in_reply_to_screen_name,
							"conversation_status":5,
							"tweet_text":test.full_text,
							"checks_made":(max_step.checks_made+1),
							"reachout_template":conversation_tree[3]
						}]
						print('LOOK HERE --------------------')
						print(to_insert)
						DB.insert_conversations(to_insert)
					except tweepy.TweepError as e:
						logging.error("Tweepy error occured:{}".format(e))
				elif location['status'] == "ZERO_RESULTS":
					pass
					return end_conversation(root_id, max_step)
		else:
			pass
	elif max_step.conversation_status == 5:
		# function to update checks
		DB.update_conversation_checks(root_id)
		print('conversation_finished')


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
