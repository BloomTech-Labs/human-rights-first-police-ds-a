""" This module holds everything related to the twitterbot """

from dotenv import load_dotenv, find_dotenv

import requests, json, os

from typing import List, Dict

from app.db import Database
import app.twitter as twitter
from app.twitter import create_api

load_dotenv(find_dotenv())
DB = Database()

MAP_API = os.getenv("MAP_API") # Maps to Google Places API

bot_name = os.getenv("BOT_NAME")  # Need bot name

bot_id = 1436057566807674897

welcome_message_id = 1440023048313131014


dm_link = f'https://twitter.com/messages/compose?recipient_id={bot_id}&welcome_message_id={welcome_message_id}'

conversation_tree = {
	1: "Hey, I'm working on the behalf of Blue Witness, can you give me more information regarding the incident you tweeted?",
	10: "Click link below to start conversation.",
	11: "Thank you for your contribution. Please fill out this form.",
	13: "Thanks anyway!"
} # These are the conversation statements the bot executes based on the max step of the conversation



def send_form(data: Dict):
	"""
	Sends additional information form to user in tweet 
	OR starts a conversation with user using bot
	AND Progresses through conversation based on the
	step counted by the Postgres Table
	"""

	to_insert = DB.convert_invocation_conversations(data)
	form_link = f'https://a.humanrightsfirst.dev/edit/{to_insert.incident_id}'
	to_insert.checks_made = 1
	

	if to_insert.form == 0:  # if the form request is 0; send tweet w/ form link and updates conversations table
		to_insert.tweet_text = '@' + to_insert.in_reply_to_id + ' ' + conversation_tree[1] + '\n' + form_link
		to_insert.reachout_template = conversation_tree[1]
		status = twitter.respond_to_tweet(to_insert.tweet_id, to_insert.tweet_text)
		to_insert.conversation_status = 0
		to_insert.tweeter_id = bot_name
		to_insert.sent_tweet_id = status.id
		DB.insert_data_conversations([to_insert])

	else: # If the form is 1; Twitter bot sends dm request to start conversation to gather info. 
		to_insert.tweet_text = '@' + to_insert.in_reply_to_id + ' ' + conversation_tree[10] + '\n' + dm_link
		to_insert.reachout_template = conversation_tree[10]
		status = twitter.respond_to_tweet(to_insert.tweet_id, to_insert.tweet_text)
		to_insert.conversation_status = 10
		to_insert.tweeter_id = bot_name
		to_insert.sent_tweet_id = status.id
		DB.insert_data_conversations(to_insert)


def receive_form(data: Dict):
	""" 
	Takes input from user/POST
	AND inputs into conversations table
	if no root_id with conversation_status 7 
	"""

	to_insert = DB.convert_form_conversations(data)
	to_insert.conversation_status = 12
	validation_check = DB.get_root_twelve(data.tweet_id)
	if len(validation_check) == 0:
	# If we don't have a value, we can add 1
		DB.insert_data_conversations(to_insert)


def advance_all():
	"""
	Advances all conversations based on highest 
	conversations status per tweet_id in Conversations Table
	"""
	to_advance = DB.get_to_advance()
	for threads in to_advance:
		advance_conversation(threads.tweet_id)


def end_conversation(root_id: int, max_step: List, received_tweet_id=None):
	# TODO Currently not in use, Refactor as you see fit
	""" Ends conversation of given root, sets conversation_status to 5 """
	api = create_api()
	if received_tweet_id:
		other_person = api.get_status(received_tweet_id)
	else:
		other_person = api.get_status(max_step.received_tweet_id)

	other_person = other_person.screen_name
	test = twitter.get_replies(bot_name, max_step.sent_tweet_id, other_person)
	if test:

		status = twitter.respond_to_tweet(test.id_str, conversation_tree[4])

		max_step.tweet_id = root_id
		max_step.receive_tweet_id = test.id_str
		max_step.in_reply_to_id = status.in_reply_to_status_id
		max_step.tweeter_id = test.in_reply_to_screen_name
		max_step.conversation_status = 5
		max_step.checks_made = (max_step.checks_made+1)
		max_step.reachout_template = conversation_tree[4]

		DB.insert_data_conversations(max_step)

	else:
		pass


def advance_conversation(root_id: int, form_link: str = None) -> str:
	""" Advances conversation by root_id """
	api = create_api()
	root_conversation = DB.get_conversation_root(root_id)

	for steps in root_conversation: # This checks every item in Conversations Table by tweet id

		max_step = steps
	if max_step.conversation_status == 0 and max_step.form == 0:
		# Technically our form handles this with quick replies
		# This is really for conversation processing 
		status = twitter.respond_to_tweet(max_step.tweet_id, conversation_tree[1])
		
		max_step.tweet_id = root_id
		max_step.sent_tweet_id = status.id_str
		max_step.in_reply_to_id = status.in_reply_to_status_id
		max_step.conversation_status = (max_step.conversation_status+1)
		max_step.checks_made = (max_step.checks_made+1)
		max_step.reachout_template = conversation_tree[1]

		DB.insert_data_conversations(max_step)
	elif max_step.conversation_status == 0 and max_step.form == 1:
		status = twitter.respond_to_tweet(max_step.tweet_id, max_step.form_link)

		max_step.tweet_id = root_id
		max_step.sent_tweet_id = status.id_str
		max_step.in_reply_to_id = status.in_reply_to_status_id
		max_step.conversation_status = 4
		max_step.checks_made = (max_step.checks_made+1)
		max_step.reachout_template = form_link

		DB.insert_data_conversations(max_step)
	# Possible TODO Classification or NLP Model can be implemented here for tweet responses	
	elif max_step.conversation_status == 1 and max_step.form == 0:

		test = twitter.get_replies(bot_name, max_step.sent_tweet_id, max_step.tweeter_id)
		if test:
			if test.full_text == '@' + bot_name + 'Yes':
				status = twitter.respond_to_tweet(test.id_str,conversation_tree[2])
				
				max_step.tweet_id = root_id
				max_step.received_tweet_id = test.id_str
				max_step.in_reply_to_id = status.in_reply_to_status_id
				max_step.tweeter_id = test.in_reply_to_screen_name
				max_step.conversation_status = (max_step.conversation_status+1)
				max_step.tweet_text = test.full_text
				max_step.checks_made = (max_step.checks_made+1)
				max_step.reachout_template = conversation_tree[2]
				
				DB.insert_data_conversations(max_step)

				return test
			elif test.full_text == "@" + bot_name + 'No':                           ### INSERT CLASSIFICATION MODEL CALL HERE ####
				end_conversation(root_id, max_step, received_tweet_id=test.id_str)
			else:                                                                   ### INSERT CLASSIFICATION MODEL HERE (MAYBE CASE)
				end_conversation(root_id, max_step, received_tweet_id=test.id_str)
		else:
			pass	

	elif max_step.conversation_status == 5:
		DB.update_conversation_checks(root_id)
	# Begins Conversation Flow 
	elif max_step.conversation_status == 10:

		processed_dms = twitter.process_dms(user_id=max_step.in_reply_to_id, tweet_id=max_step.tweet_id, incident_id=max_step.incident_id, convo_tree_txt=conversation_tree[11])
		if processed_dms is not None:
	
			max_step.tweet_text = processed_dms['quick_reply_response']
			max_step.reachout_template = conversation_tree[11]
			max_step.checks_made= (max_step.checks_made+1)
			max_step.conversation_status = processed_dms['conversation_status']

			DB.insert_data_conversations(max_step)


	elif max_step.conversation_status == 12:
		# This is a holder for approvals on the admin end
		DB.update_conversation_checks(root_id)

	elif max_step.conversation_status == 13:
		DB.update_conversation_checks(root_id)


def clean_query_string(string: str) -> str:
	""" Cleans string of ' 's and 's """
	string.replace(' ', '%20')
	string.replace(',', '')
	return string


def find_location(query_string: str) -> Dict:
	""" Makes call to google places api """
	query_string = clean_query_string(query_string)
	query='https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=formatted_address,geometry,name,place_id&key={}'.format(query_string, MAP_API)
	resp = requests.get(query)
	data = json.loads(resp.content)
	return data
