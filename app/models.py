from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, List, Dict

Base = declarative_base()


class ForceRanks(Base):

    __tablename__ = "force_ranks"

    incident_id = Column(Integer, primary_key=True,
                         nullable=False, unique=True)
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
    children = relationship("Conversations", back_populates="parent")

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


class Conversations(Base):

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer, ForeignKey('force_ranks.incident_id'))
    tweet_id = Column(String(255))
    form = Column(Integer)
    root_tweet_city = Column(String(255))
    root_tweet_state = Column(String(255))
    root_tweet_lat = Column(Float)
    root_tweet_long = Column(Float)
    root_tweet_date = Column(Date)
    root_tweet_force_rank = Column(String(255), default=None)
    sent_tweet_id = Column(String)
    received_tweet_id = Column(String)
    in_reply_to_id = Column(String)
    tweeter_id = Column(String)
    conversation_status = Column(Integer)
    tweet_text = Column(String)
    checks_made = Column(Integer)
    reachout_template = Column(String)
    isChecked = Column(Boolean)
    parent = relationship("ForceRanks", back_populates="children")
    id = Column(Integer, primary_key=True)
    root_tweet_id = Column(String)
    sent_tweet_id = Column(String)
    received_tweet_id = Column(String)
    in_reply_to_id = Column(String)
    tweeter_id = Column(String)
    conversation_status = Column(Integer)
    tweet_text = Column(String)
    checks_made = Column(Integer)
    reachout_template = Column(String)

    def __repr__(self):
        return(
            "id:{}, tweet_id:{}, form:{}, root_tweet_city:{}, root_tweet_state:{}, root_tweet_lat:{}, root_tweet_long:{}, root_tweet_date:{}, root_tweet_force_rank:{}, sent_tweet_id:{}, received_tweet_id:{}, in_reply_to_id:{}, tweeter_id:{}, conversation_state:{}, tweet_text:{}, checks_made:{}, reachout_template:{}, isChecked:{}").format(
            self.id,
            self.tweet_id,
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


class form_out(BaseModel):
    form: int
    incident_id: int
    isChecked: bool
    link: str
    tweet_id: str
    user_name: str


class form_in(BaseModel):
    city: str
    state: str
    confidence: Optional[float] = 0
    description: str
    force_rank: str
    incident_date: str
    incident_id: int
    lat: Optional[float] = None
    long: Optional[float] = None
    src: List[str] = []

    status: str
    title: str
    tweet_id: str
    user_name: str


class check(BaseModel):
    tweet_id: str
