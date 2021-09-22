""" This module should hold everything related to the twitterbot """

from dotenv import load_dotenv, find_dotenv

import requests, json, os

from typing import List, Dict

from app.db import Database
import app.twitter as twitter
from app.twitter import create_api

load_dotenv(find_dotenv())
DB = Database

MAP_API = os.getenv("MAP_API")

bot_name = os.getenv("BOT_NAME")  # Need bot name

bot_id = 1436057566807674897

welcome_message_id = 1440023048313131014

dm_link = f'https://twitter.com/messages/compose?recipient_id={bot_id}&welcome_message_id={welcome_message_id}'

conversation_tree = {
	1: "Hey, This is a test.",
	# 2:"Do you want to fill out a form or talk with the bot",
	# 3:"What is the location where this incident took place?",
	# 4:"What is the date",
	# 5:"what is the force_rank, here are the options",
	# 6:"Thanks! You're helping (align incentives)!",
	# 7:"Thanks anyway!",
	# 8:"Please fill out this form ",

	10: 'Click link below to start conversation ',
	11: 'Please fill out this form ',
	13: 'Thanks anyway!'
}


def send_form(data: Dict):
	"""
	Sends form to user in tweet or starts bot conversation based on form,
	inserts to conversations table
	"""

	to_insert = DB.convert_invocation_conversations(data)
	incident_id = to_insert['incident_id']
	user_id_str = twitter.get_user_id_from_tweet(to_insert['tweet_id'])
	form_link = f'https://a.humanrightsfirst.dev/edit/{incident_id}'
	to_insert['tweet_id'] = int(to_insert['tweet_id'])
	to_insert['in_reply_to_id'] = to_insert['tweeter_id']
	del to_insert['link']
	to_insert['checks_made'] = 1
	

	if to_insert['form'] == 0:
		to_insert['tweet_text'] = '@' + to_insert['tweeter_id'] + ' ' + conversation_tree[1] + '\n' + form_link
		to_insert['reachout_template'] = conversation_tree[1]
		status = twitter.respond_to_tweet(to_insert['tweet_id'], to_insert['tweet_text'])
		to_insert['conversation_status'] = 0
		to_insert['tweeter_id'] = bot_name
		to_insert['sent_tweet_id'] = status.id
		DB.insert_data_conversations([to_insert])

	else:
		to_insert['tweet_text'] = '@' + to_insert['tweeter_id'] + ' ' + conversation_tree[10] + '\n' + dm_link
		to_insert['reachout_template'] = conversation_tree[10]
		status = twitter.respond_to_tweet(to_insert['tweet_id'], to_insert['tweet_text'])
		to_insert['conversation_status'] = 10
		to_insert['tweeter_id'] = bot_name
		to_insert['sent_tweet_id'] = status.id
		DB.insert_data_conversations([to_insert])


def receive_form(data: Dict):
	""" Takes input from user/POST inputs into conversations if no root_id with conversation_status 7 """

	to_insert = DB.convert_form_conversations(data)
	to_insert['tweet_id'] = int(to_insert['tweet_id'])
	to_insert['conversation_status'] = 12
	validation_check = DB.get_root_twelve(to_insert['tweet_id'])
	if len(validation_check) == 0:
		DB.insert_data_conversations([to_insert])


def advance_all():
	""" Advances all conversations based on highest conversations status per tweet_id """
	to_advance = DB.get_to_advance()
	for threads in to_advance:
		advance_conversation(threads.tweet_id)


def end_conversation(root_id: int, max_step: List, received_tweet_id=None):
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
		to_insert = [{
			"tweet_id":root_id,
			"sent_tweet_id":max_step.sent_tweet_id,
			"received_tweet_id":test.id_str,
			"in_reply_to_id":test.in_reply_to_status_id,
			"tweeter_id":test.in_reply_to_screen_name,
			"conversation_status":5,
			"tweet_text":test.full_text,
			"checks_made":(max_step.checks_made+1),
			"reachout_template":conversation_tree[4]
		}]
		DB.insert_data_conversations(to_insert)
	else:
		pass


def advance_conversation(root_id: int, form_link: str = None) -> str:
	""" Advances conversation by root_id """
	api = create_api()
	root_conversation = DB.get_conversation_root(root_id)
	max = -1

	for steps in root_conversation:

		if steps.conversation_status > max:
			max = steps.conversation_status
			max_step = steps
	if max_step.conversation_status == 0 and max_step.form == 0:
		status = twitter.respond_to_tweet(max_step.tweet_id, conversation_tree[1])
		to_insert = [{
			"tweet_id":root_id,
			"sent_tweet_id":status.id_str,
			"in_reply_to_id":status.in_reply_to_status_id,
			"tweeter_id":max_step.tweeter_id,
			"conversation_status":(max_step.conversation_status+1),
			"tweet_text":max_step.tweet_text,
			"checks_made":(max_step.checks_made+1),
			"reachout_template":conversation_tree[1],
			"form":0
		}]

		DB.insert_data_conversations(to_insert)
	elif max_step.conversation_status == 0 and max_step.form == 1:
		status = twitter.respond_to_tweet(max_step.tweet_id, max_step.form_link)

		to_insert = [{
			"tweet_id":root_id,
			"sent_tweet_id":status.id_str,
			"in_reply_to_id":status.in_reply_to_status_id,
			"tweeter_id":max_step.tweeter_id,
			"conversation_status":4,
			"tweet_text":max_step.tweet_text,
			"checks_made":(max_step.checks_made+1),
			"reachout_template":form_link,
			"form":1
		}]

		DB.insert_data_conversations(to_insert)
	elif max_step.conversation_status == 1 and max_step.form == 0:

		test = twitter.get_replies(bot_name, max_step.sent_tweet_id, max_step.tweeter_id)
		if test:
			if test.full_text == '@' + bot_name + 'Yes': ### INSERT CLASSIFICATION MODEL CALL HERE ####
				status = twitter.respond_to_tweet(test.id_str,conversation_tree[2])
				to_insert = [{
					"tweet_id":root_id,
					"sent_tweet_id":max_step.sent_tweet_id,
					"received_tweet_id":test.id_str,
					"in_reply_to_id":test.in_reply_to_status_id,
					"tweeter_id":test.in_reply_to_screen_name,
					"conversation_status":(max_step.conversation_status+1),
					"tweet_text":test.full_text,
					"checks_made":(max_step.checks_made+1),
					"reachout_template":conversation_tree[2],
					"form":0
				}]

				DB.insert_data_conversations(to_insert)
				return test
			elif test.full_text == "@" + bot_name + 'No':                           ### INSERT CLASSIFICATION MODEL CALL HERE ####
				end_conversation(root_id, max_step, received_tweet_id=test.id_str)
			else:                                                                   ### INSERT CLASSIFICATION MODEL HERE (MAYBE CASE)
				end_conversation(root_id, max_step, received_tweet_id=test.id_str)
		else:
			pass
	elif max_step.conversation_status == 2 and max_step.form == 0:

		other_person = api.get_status(max_step.received_tweet_id)
		other_person = other_person.user.screen_name
		test = twitter.get_replies(bot_name, max_step.sent_tweet_id, other_person)

		if test is not None:

			if test.full_text:
				location = find_location(test.fill_text.lstrip("@" + bot_name + " "))

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
					DB.update_force_rank_location(update_data, root_id)
					status = twitter.respond_to_tweet(max_step.tweeter_id, conversation_tree[3])
					to_insert = [{
						"tweet_id":root_id,
						"sent_tweet_id":max_step.sent_tweet_id,
						"received_tweet_id":test.id_str,
						"in_reply_to_id":test.in_reply_to_status_id,
						"tweeter_id":test.in_reply_to_screen_name,
						"conversation_status":5,
						"tweet_text":test.full_text,
						"checks_made":(max_step.checks_made+1),
						"reachout_template":conversation_tree[3],
						"form":0
					}]

					DB.insert_data_conversations(to_insert)
				elif location['status'] == "ZERO_RESULTS":
					pass
					return end_conversation(root_id, max_step)
		else:
			pass

	elif max_step.conversation_status == 5:
		DB.update_conversation_checks(root_id)
	elif max_step.conversation_status == 10:

		processed_dms = twitter.process_dms(user_id=max_step.in_reply_to_id, tweet_id=max_step.tweet_id, incident_id=max_step.incident_id, convo_tree_txt=conversation_tree[11])
		if processed_dms is not None:

			to_insert = {}
			to_insert["incident_id"] = max_step.incident_id
			to_insert["form"] = max_step.form
			to_insert['tweeter_id'] = processed_dms['tweeter_id']
			to_insert['tweet_text'] = processed_dms['quick_reply_response']
			to_insert['tweet_id'] = max_step.tweet_id
			to_insert['reachout_template'] = conversation_tree[11]
			to_insert['checks_made'] = (max_step.checks_made+1)
			to_insert['conversation_status'] = processed_dms['conversation_status']

			DB.insert_data_conversations([to_insert])

	elif max_step.conversation_status == 12:
		# This is where we've received a response, shouldn't do anything here, only return when asked for directly through endpoint
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
