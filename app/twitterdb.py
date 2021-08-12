from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from sqlalchemy import create_engine, select, insert, update, func
from sqlalchemy.orm import sessionmaker, scoped_session

from models import Conversations, ForceRanks, DirectMessages

DB_CONN_STR = os.getenv("DB_URL")


class Database(object):

	def __init__(self):
		self.engine = create_engine(
			DB_CONN_STR,
			pool_recycle=3600,
			pool_size=10,
			echo=False,
			pool_pre_ping=True
		)

		self.Sessionmaker = scoped_session(
			sessionmaker(
				autoflush=False,
				autocommit=False,
				bind=self.engine
			)
		)

	# Conversations Queries

	def load_data_conversations(self):
		"""Get all data from conversations"""
		with self.Sessionmaker() as session:
			query = select(Conversations)
			conversations_data = session.execute(query)

		return [i[0] for i in conversations_data.fetchall()]

	def get_conversation_root(self, root_id: int):
		"""Get conversations with a specific root"""
		with self.Sessionmaker() as session:
			query = select(Conversations).where(Conversations.root_tweet_id == root_id)
			conversations_data = session.execute(query)

		return [i[0] for i in conversations_data.fetchall()]

	def insert_conversations(self, data):

		with self.Sessionmaker() as session:
			for datum in data:
				obj = Conversations(**datum)
				session.add(obj)
				session.commit()


	def get_to_advance(self):
		# for each root_id, get highest conversation_status
		with self.Sessionmaker() as session:
			query1 = select(
				func.max(Conversations.conversation_status).label("status"), 
				Conversations.root_tweet_id
			).group_by(
				Conversations.root_tweet_id
			).cte('wow')

			query2 = select(
				Conversations
			).join(
				query1, 
				query1.c.root_tweet_id==Conversations.root_tweet_id
			).filter(
				Conversations.conversation_status==query1.c.status
			)

			data = session.execute(query2)

		return [i[0] for i in data.fetchall()]

	def update_conversation_checks(self, root_id: int):
		query = (
			update(Conversations).
			where(Conversations.root_tweet_id == str(root_id)).
			values(checks_made = Conversations.checks_made + 1)
			)

		with self.Sessionmaker() as session:
			session.execute(query)
			session.commit()

	# Force Rank Queries


	def load_data_force_rank(self):

		with self.Sessionmaker() as session:
			query = select(ForceRanks)
			force_ranks_data = session.execute(query)
			
		return force_ranks_data.fetchall()


	def get_no_location_force_rank(self):

		with self.Sessionmaker() as session:
			query = select(ForceRanks).filter(ForceRanks.like("%Rank 0 - Test"))
			force_ranks_data = session.execute(query)
			
		return force_ranks_data.fetchall()

	def insert_force_rank(self, data):

		with self.Sessionmaker() as session:
			for datum in data:
				obj = ForceRanks(**datum)
				session.add(obj)
				session.commit()

	def update_force_rank_location(self, data, tweet_id):

		query = (
			update(ForceRanks).
			where(ForceRanks.tweet_id==str(tweet_id)).
			values(**data)
		)

		with self.Sessionmaker() as session:
			print(query.compile(), data, tweet_id)
			session.execute(query)
			session.commit()