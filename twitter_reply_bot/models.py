from sqlalchemy import Table, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Conversations(Base):

	__tablename__ = "conversations"

	id = Column(Integer, primary_key=True)
	root_tweet_id = Column(String)
	sent_tweet_id =	Column(String)
	received_tweet_id = Column(String)
	in_reply_to_id = Column(String)
	tweeter_id = Column(String)
	conversation_status = Column(Integer)
	tweet_text = Column(String)
	checks_made = Column(Integer)
	reachout_template = Column(String)


class ForceRanks(Base):

	__tablename__ = "force_ranks"

	incident_id = Column(Integer, primary_key=True, nullable=False)
	incident_date = Column(Date, nullable=False)
	tweet_id = Column(String(255))
	user_name = Column(String(255))
	description = Column(String(10000), nullable=False)
	city = Column(String(255), default=None)
	state = Column(String(255), default=None)
	lat = Column(Float)
	long = Column(Float)
	title = Column(String(255), default=None)
	force_rank = Column(String(255), nullable=False)
	status = Column(String(255), default='pending', nullable=False)
	confidence = Column(Float)
	tags = Column(String(255))
	src = Column(String(8000))
