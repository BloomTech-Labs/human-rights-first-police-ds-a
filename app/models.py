from sqlalchemy import Table, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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
