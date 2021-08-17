from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import requests, time, json, re
import os, logging, tweepy
from typing import Tuple, List, Dict
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, insert, update, func

from app.scraper import DB
import app.twitter as twitter


MAP_API = os.getenv("MAP_API")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

bot_name = 'RowenWitt' # Need bot name

conversation_tree = {
	1:"Hi, do you have more information about the location of this incident?",
	2:"What is the location where this incident took place?",
	3:"Thanks! You're helping (align incentives)!",
	4:"Thanks anyway!",
	5:"Please fill out this form "
}

# test_entries = [
# 	{"root_tweet_id":"1424511565932359685","tweeter_id":"witt_rowen","conversation_status":0,"tweet_text":"Incident report test 1 🦟📡","checks_made":0},
# 	{"root_tweet_id":"1424420702208237573","tweeter_id":"witt_rowen","conversation_status":0,"tweet_text":"Incident report test 2 🐥","checks_made":0},
# 	{"root_tweet_id":"1424452159744077826","tweeter_id":"witt_rowen","conversation_status":0,"tweet_text":"Incident report test 3🦧","checks_made":0},
# ]

test_entries = [
	{"form":1,"incident_id":1,"isChecked":False,"link":"https://a.humanrightsfirst.dev/edit/1426290795267731463","tweet_id":"1424511565932359685","user_name":"witt_rowen"}
]

test_insert = [
	{"city":"TestTown","confidence":None,"dsecription":"testtest","force_rank":"Rank - 1 Police Presence","incident_date":"2021-04-22T00:00:00.000Z","incident_id":1,"lat":42.64249,"long":-73.7576,"src":[],"tags":["police","bacon","general_pork_products"],"title":"testers","tweet_id":"1424511565932359685","user_name":"witt_rowen"}
]


def send_form(data:Dict):
	""" Sends form to user, inserts to conversations table """

	to_insert = DB.convert_invocation_conversations(data)
	to_insert['root_tweet_id'] = int(to_insert['root_tweet_id'])
	to_insert['tweet_text'] = '@' + to_insert['user_name'] + ' ' + conversation_tree[5] + to_insert['link'] 
	to_insert['reachout_template'] = conversation_tree[5]
	del to_insert['link']
	del to_insert['user_name']
	try:
		status = twitter.respond_to_tweet(to_insert['root_tweet_id'], to_insert['tweet_text'])
		to_insert['tweeter_id'] = bot_name
		to_insert['isChecked'] = True
		to_insert['conversation_status'] = 6
		to_insert['checks_made'] = 1
		to_insert['sent_tweet_id'] = status.id,

		DB.insert_data_conversations([to_insert])
	except tweepy.TweepError as e:
		logging.error("Tweepy error occured:{}".format(e))


def receive_form(data:Dict):
	""" Takes input from user/POST inputs into conversations if no root_id with conversation_status 7 """

	to_insert = DB.convert_form_conversations(data)
	to_insert['root_tweet_id'] = int(to_insert['root_tweet_id'])
	to_insert['isChecked'] = True
	to_insert['conversation_status'] = 7
	validation_check = DB.get_root_seven(to_insert['root_tweet_id'])
	if len(validation_check) == 0:
		DB.insert_data_conversations([to_insert])


def advance_all():
	""" Advances all conversations based on highest conversations status per root_tweet_id """
	to_advance = DB.get_to_advance()
	for threads in to_advance:
		advance_conversation(points.root_tweet_id)
		print('success', threads.root_tweet_id)  # DELETE BEFORE PR


def reset_conversations_for_test():   # DELETE BEFORE PR
	DB.reset_conversations()   # DELETE BEFORE PR
	DB.insert_data_conversations(test_entries)   # DELETE BEFORE PR
	print("done, you idiot")   # DELETE BEFORE PR


def end_conversation(root_id: int, max_step: List, received_tweet_id=None):
	""" Ends conversation of given root, sets conversation_status to 5 """
	print("\n", "\n", "\n", max_step.__dict__)  # DELETE BEFORE PR

	if received_tweet_id:
		other_person = twitter.api.get_status(received_tweet_id)
	else:
		other_person = twitter.api.get_status(max_step.received_tweet_id)

	other_person = other_person.screen_name
	test = twitter.get_replies(bot_name, max_step.sent_tweet_id, other_person)
	if test:
		try:
			status = twitter.respond_to_tweet(test.id_str, conversation_tree[4])
			to_insert = [{
				"root_tweet_id":root_id,
				"sent_tweet_id":status_id,
				"received_tweet_id":test.id_str,
				"in_reply_to_id":test.in_reply_to_status_id,
				"tweeter_id":test.in_reply_to_screen_name,
				"conversation_status":5,
				"tweet_text":test.full_text,
				"checks_made":(max_step.checks_made+1),
				"reachout_template":conversation_tree[4]
			}]
			DB.insert_data_conversations(to_insert)
		except tweepy.TweepError as e:
			logging.error("Tweepy error occured:{}".format(e))
	else:
		print('error_here')   # DELETE


def advance_conversation(root_id: int, form_link: str) -> str:
	""" Advances conversation by root_id """
	root_conversation = DB.get_conversation_root(root_id)
	max = -1
	print([i.__dict__ for i in root_conversation])  # DELETE BEFORE PR
	for steps in root_conversation:
		print(steps.__dict__)  # DELETE BEFORE PR
		if steps.conversation_status > max:
			max = steps.conversation_status
			max_step = steps
			print(max_step.__dict__)  # DELETE BEFORE PR
	if max_step.conversation_status == 0 and max_step.form == 0:
		try:
			status = twitter.respond_to_tweet(max_step.root_tweet_id, conversation_tree[1])
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
				"reachout_template":conversation_tree[1],
				"form":0
			}]

			print(to_insert)  # DELETE BEFORE PR
			DB.insert_data_conversations(to_insert)
		except tweepy.TweepError as e:
			logging.error("Tweepy error occured:{}".format(e))
	elif max_step.conversation_status == 0 and max_step.form == 1:
		try:
			status = twitter.respond_to_tweet(max_step.root_tweet_id, max_step.form_link)
			print(max_step.conversation_status)  # DELETE BEFORE PR
			print(max_step.tweet_text) # DELETE BEFORE PR (SHOULD ALWAYS BE EMPTY?)
			print(max_step.reachout_template) # DELETE BEFORE PR (SHOULD ALWAYS BE EMPTY?)
			to_insert = [{
				"root_tweet_it":root_id,
				"sent_tweet_id":status.id_str,
				"in_reply_to_id":status.in_reply_to_status_id,
				"tweeter_id":max_step.tweeter_id,
				"conversation_status":4,
				"tweet_text":max_step.tweet_text,
				"checks_made":(max_step.checks_made+1),
				"reachout_template":form_link,
				"form":1
			}]

			print(to_insert)  # DELETE BEFORE PR
			DB.insert_data_conversations(to_insert)
		except tweepy.TweepError as e:
			logging.error("Tweepy error occured:{}".format(e))
	elif max_step.conversation_status == 1 and max_step.form == 0:
		print('works so far') # DELETE BEFORE PR
		test = twitter.get_replies(bot_name, max_step.sent_tweet_id, max_step.tweeter_id)
		if test:
			if test.full_text == '@' + bot_name + 'Yes': ### INSERT CLASSIFICATION MODEL CALL HERE ####
				try:
					status = twitter.respond_to_tweet(test.id_str,conversation_tree[2])
					to_insert = [{
						"root_tweet_id":root_id,
						"sent_tweet_id":status_id,
						"received_tweet_id":test.id_str,
						"in_reply_to_id":test.in_reply_to_status_id,
						"tweeter_id":test.in_reply_to_screen_name,
						"conversation_status":(max_step.conversation_status+1),
						"tweet_text":test.full_text,
						"checks_made":(max_step.checks_made+1),
						"reachout_template":conversation_tree[2],
						"form":0
					}]
					print(to_insert) # DELETE BEFORE PR
					DB.insert_data_conversations(to_insert)
					return test
				except tweepy.TweepError as e:
					logging.error("Tweepy error occured:{}".format(e))
			elif test.full_text == "@" + bot_name + 'No': ### INSERT CLASSIFICATION MODEL CALL HERE ####
				end_conversation(root_id, max_step, received_tweet_id=test.id_str)
			else:  ### INSERT CLASSIFICATION MODEL HERE (MAYBE CASE)
				end_conversation(root_id, max_step, received_tweet_id=test.id_str)
		else:
			pass
	elif max_step.conversation_status == 2 and max_step.form == 0:
		print('We got this far')  # DELETE BEFORE PR
		print(max_step) # DELETE BEFORE PR
		other_person = twitter.api.get_status(max_step.received_tweet_id)
		other_person = other_person.user.screen_name
		test = twitter.get_replies(bot_name, max_step.sent_tweet_id, other_person)

		if test is not None:
			print(test.full_text) # DELETE BEFORE PR
			if test.full_text: ### VALIDATION GOES HERE ####
				location = find_location(test.fill_text.lstrip("@" + bot_name + " "))
				print(location) # DELETE BEFORE PR
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
					try:
						status = twitter.respond_to_tweet(test_id, conversation_tree[3])
						to_insert = [{
							"root_tweet_id":root_id,
							"sent_tweet_id":status_id,
							"received_tweet_id":test.id_str,
							"in_reply_to_id":test.in_reply_to_status_id,
							"tweeter_id":test.in_reply_to_screen_name,
							"conversation_status":5,
							"tweet_text":test.full_text,
							"checks_made":(max_step.checks_made+1),
							"reachout_template":conversation_tree[3],
							"form":0
						}]
						print(to_insert) # DELETE BEFORE PR
						DB.insert_data_conversations(to_insert)
					except tweepy.TweepError as e:
						logging.error("Tweepy error occured:{}".format(e))
				elif location['status'] == "ZERO_RESULTS":
					pass
					return end_conversation(root_id, max_step)
		else:
			pass

	elif max_step.conversation_status == 5:
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
