from pydantic import BaseModel
from sqlalchemy import Column, Date, Float, Integer, String, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class RequestedFormData(BaseModel):
    tweet_source: str
    information_requested: str


class DirectMessages(Base):

    __tablename__ = 'direct_messages'

    id = Column(Integer, primary_key=True)
    created_timestamp = Column(Date, nullable=False)
    welcome_message_id = Column(String, nullable=False)
    sender_id = Column(String, nullable=False)
    dm_text = Column(String)
    quick_reply_response = Column(String)


class Form(Base):

    __tablename__ = 'form'

    id = Column(Integer, primary_key=True, ForeignKey='incident.id', nullable=False)
    form_type = Column(String, nullable=False)
    source_tweet_id = Column(String, nullable=False)
    response_city = Column(String, default=None)
    response_state = Column(String, default=None)
    response_force_rank = Column(Integer, default=None)
    response_YN_force = Column(Boolean, default=None)
    force_ranks = relationship('ForceRanks', back_populates='form')

class Conversations(Base):

	__tablename__ = "conversations"

	id = Column(Integer, primary_key=True)
	root_tweet_id = Column(String)
	form = Column(Integer)
	root_tweet_city = Column(String(255))
	root_tweet_state = Column(String(255))
	root_tweet_lat = Column(Float)
	root_tweet_long = Column(Float)
	root_tweet_date = Column(Date)
	root_tweet_force_rank = Column(String(255), default=None)
	sent_tweet_id =	Column(String)
	received_tweet_id = Column(String)
	in_reply_to_id = Column(String)
	tweeter_id = Column(String)
	conversation_status = Column(Integer)
	tweet_text = Column(String)
	checks_made = Column(Integer)
	reachout_template = Column(String)
	isChecked = Column(Boolean)


	def __repr__(self):
		return(
			"id:{}, root_tweet_id:{}, form:{}, root_tweet_city:{}, root_tweet_state:{}, root_tweet_lat:{}, root_tweet_long:{}, root_tweet_date:{}, root_tweet_force_rank:{}, sent_tweet_id:{}, received_tweet_id:{}, in_reply_to_id:{}, tweeter_id:{}, conversation_state:{}, tweet_text:{}, checks_made:{}, reachout_template:{}, isChecked:{}").format(
			self.id,
			self.root_tweet_id,
			self.form,
			self.root_tweet_city,
			self.root_tweet_state,
			self.root_tweet_lat,
			self.root_tweet_long,
			self.root_tweet_date,
			self.root_tweet_force_rank,
			self.sent_tweet_id,
			self.received_tweet_id,
			self.in_reply_to_id,
			self.tweeter_id,
			self.conversation_status,
			self.tweet_text,
			self.checks_made,
			self.reachout_template,
			self.isChecked
			)


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
    force_rank = Column(String(255), default=None)
    status = Column(String(255), default='pending', nullable=False)
    confidence = Column(Float)
    tags = Column(String(255))
    src = Column(String(8000))
    form = relationship("Form", back_populates="force_ranks")

    def __repr__(self):
        return (
            "incident_id:{}, incident_date:{}, tweet_id:{}, user_name:{}, description:{}, city:{}, state:{}, lat:{}, long:{}, title:{}, force_rank:{}, status:{}, confidence:{}, tags:{}, src:{}").format(
            self.incident_id,
            self.incident_date,
            self.tweet_id,
            self.user_name,
            self.description,
            self.city,
            self.state,
            self.lat,
            self.long,
            self.title,
            self.force_rank,
            self.status,
            self.confidence,
            self.tags,
            self.src
        )
