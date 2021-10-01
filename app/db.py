"""
This module should should hold everything related to the database including:
- Connections
- Queries
- Bot Scripts

Declarative_base:
https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base

Sessions:
https://docs.sqlalchemy.org/en/14/orm/session_basics.html#using-a-sessionmaker

Scoped session:
https://docs.sqlalchemy.org/en/14/orm/contextual.html

Typing:
https://docs.python.org/3/library/typing.html

"""

from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import table
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship, sessionmaker, scoped_session

from dotenv import load_dotenv, find_dotenv
from random import random as rand
import os

from sqlalchemy import create_engine, inspect, select, update, func, and_
from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey

from typing import List, Dict

load_dotenv(find_dotenv())

db_url = os.getenv("DB_URL")

# connects to database for SQL operations,echo generates the activity log
engine = create_engine(db_url, echo=True)

"""describes db tables and defines classes that 
   will be mapped to those tables"""
Base = declarative_base()


class ForceRanks(Base):
    """
    Describe the Postgres table AND
    maps a path to those tablesn
    """
    __tablename__ = "force_ranks"  

    incident_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        unique=True)
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
        return "incident_id:{}, incident_date:{}, tweet_id:{}, user_name:{}, description:{}, city:{}, state:{}, lat:{}, long:{}, title:{}, force_rank:{}, status:{}, confidence:{}, tags:{}, src:{}".format(
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

    def __repr__(self):
        return (
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


class Training(Base):
    __tablename__ = "training"

    id = Column(Integer, primary_key=True)
    tweets = Column(String)
    labels = Column(Integer)

    def __repr__(self):
        return (
            "id:{}, tweets:{}, labels:{}"
        ).format(self.id, self.tweets, self.labels)


class Database(object):

    def __init__(self):
        self.engine = create_engine(
            db_url,
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

        self.TABLE_NAMES = {"force_ranks": ForceRanks,
                            "conversations": Conversations,
                            }

    def get_conversation_root(self, root_id: int):
        """ Get conversation with a specific root_tweet_id """
        with self.Sessionmaker() as session:
            query = select(Conversations).where(
                Conversations.tweet_id == root_id)
            conversations_data = session.execute(query)
        return [i[0] for i in conversations_data.fetchall()]


    def get_sripts_per_node(self, convo_node):
        """
        Gets scripts and their ids, use counts and success rates for a given
        conversation node all for the use of the script selection process.
        """
        with self.Sessionmaker() as session:
            query = (
                select(BotScripts.script_id,
                       BotScripts.script,
                       BotScripts.use_count,
                       BotScripts.success_rate
                       ).where(BotScripts.convo_node == convo_node)
            )

            scripts = session.execute(query).fetchall()

        return scripts

    def bump_use_count(self, script_id, new_count):
        """ Updates the use_count for a script as identified by script_id """
        with self.Sessionmaker() as session:
            count_dict = {"use_count": new_count}
            query = (
                update(BotScripts).where(
                    BotScripts.script_id == script_id).values(**count_dict)
            )

            session.execute(query)
            session.commit()

    def update_pos_and_success(self, script_id, positive_count, success_rate):
        """ Updates the positive_count and success_rate for a given script_id """
        with self.Sessionmaker() as session:
            data = {"positive_count": positive_count,
                    "success_rate": success_rate
                    }
            query = update(BotScripts).where(
                BotScripts.script_id == script_id
            ).values(**data)

            session.execute(query)
            session.commit()

    def insert_data_force_ranks(self, data: List[Dict]):
        """ inserts data into force_ranks """
        with self.Sessionmaker() as session:
            last = select(func.max(ForceRanks.incident_id))
            last_value = session.execute(last).fetchall()[0][0]
            for i in range(len(data)):
                if last_value is None:
                    last_value = 0
                last_value += 1
                data[i]['incident_id'] = last_value
                if type(data[i]['confidence']) != float \
                        and data[i]['confidence'] is not None:
                    data[i]['confidence'] = data[i]['confidence'].item()
                obj = ForceRanks(**data[i])
                session.add(obj)
                session.commit()

    def insert_data_conversations(self, data):
        """ inserts data into conversations """
        with self.Sessionmaker() as session:
            last = select(func.max(Conversations.id))
            last_value = session.execute(last).fetchall()[0][0]
            if last_value is None:
                last_value = 0
            if data.id is None:
                last_value += 1
                data.id = last_value
            session.add(data)
            session.commit()

    def update_tables(self, data, tweet_id, tablename):
        """ updates table 'tablename' columns of matching tweet_id """
        if tablename == 'ForceRanks':
            table = ForceRanks
        elif tablename == 'Conversations':
            table = Conversations
        else:
            return

        query = update(table).where(
            table.tweet_id == str(tweet_id)
        ).values(**data)

        with self.Sessionmaker() as session:
            session.execute(query)
            session.commit()

    def get_root_twelve(self, root_id):
        """ gets root_ids with value of 12 """
        with self.Sessionmaker() as session:
            query = (select(Conversations).
                     filter(and_(Conversations.tweet_id == str(root_id),
                                 Conversations.conversation_status == 12)))
            check_data = session.execute(query)

        return check_data.fetchall()

    def get_root_twelve_majority(self, root_id, action):
        """ gets data on differences on incident id for admin review"""
        with self.Sessionmaker() as session:
            if action == 0:
                """Summarizes the all city, state, and date numbers that are associated with an incident_id"""
                subjects = ['root_tweet_city', 'root_tweet_state',
                            'incident_date']
                reconcilation_dict = {}
                for index, sub in enumerate(subjects):
                    query = f"""
                        select count({sub}), {sub} from 
                        (select * from conversations 
                        as c inner join force_ranks 
                        as fr on c.incident_id = fr.incident_id 
                        where c.incident_id = {root_id}) as subquery
                        group by {sub}
                        """
                    check_data = session.execute(query).fetchall()
                    reconcilation_dict[f"{index}"] = check_data
                return reconcilation_dict
            elif action == 1:
                """ Brings all the tweet-ids that are associated with the incident_id """
                query = (select(Conversations.tweet_id).
                         filter(Conversations.incident_id == root_id))
                data = session.execute(query).fetchall()
                return data
            elif action == 2:
                """ Brings the total number of incident ids in the conversations table """
                query = select(func.count(Conversations.incident_id).filter(
                    Conversations.incident_id == root_id))
                data = session.execute(query).fetchall()
                return data
            else:
                return 'Pass 0, 1, 2'

    def get_twelves(self):
        """
        get all conversations with value of 12
        and corresponding data from force_ranks
        """
        with self.Sessionmaker() as session:
            query = (select(Conversations, ForceRanks).
                     join(ForceRanks,
                          and_(Conversations.tweet_id == ForceRanks.tweet_id,
                               Conversations.conversation_status == 12)))
            data = session.execute(query).fetchall()

        out = []
        for i in data:
            record = {'tweet_id': i['Conversations'].tweet_id,
                      'city': i['Conversations'].root_tweet_city,
                      'confidence': None,
                      'description': i['ForceRanks'].description,
                      'force_rank': i['Conversations'].root_tweet_force_rank,
                      'incident_date': i['Conversations'].root_tweet_date,
                      'incident_id': i['ForceRanks'].incident_id,
                      'lat': i['Conversations'].root_tweet_lat,
                      'long': i['Conversations'].root_tweet_long}
            try:
                record['src'] = {e: i for (e, i) in enumerate(
                    i['ForceRanks'].src.replace('"', '', ).replace('[',
                                                                   '').replace(
                        ']', '').split(','))}
            except (KeyError, AttributeError):
                pass
            record['state'] = i['Conversations'].root_tweet_state
            record['status'] = i['ForceRanks'].status
            try:
                record['tags'] = {e: i for (e, i) in enumerate(
                    i['ForceRanks'].tags.replace('"', '', ).replace('[',
                                                                    '').replace(
                        ']', '').split(','))}
            except (KeyError, AttributeError):
                pass
            print(i['ForceRanks'].tags)
            record['title'] = i['ForceRanks'].title
            record['user_name'] = i['ForceRanks'].user_name
            out.append(record)

        return out

    def get_to_advance(self):
        """ gets highest conversation_status row of each tweet_id """
        with self.Sessionmaker() as session:
            query1 = select(
                func.max(Conversations.conversation_status).label("status"),
                Conversations.tweet_id
            ).group_by(
                Conversations.tweet_id
            ).cte('wow')

            query2 = select(
                Conversations
            ).join(
                query1,
                query1.c.tweet_id == Conversations.tweet_id
            ).filter(
                Conversations.conversation_status == query1.c.status
            )

            data = session.execute(query2)

        return [i[0] for i in data.fetchall()]

    def update_conversation_checks(self, root_id):
        """ iterates conversation_checks column of matching tweet_id """
        query = update(Conversations).where(
            Conversations.tweet_id == str(root_id)
        ).values(checks_made=Conversations.checks_made + 1)

        with self.Sessionmaker() as session:
            session.execute(query)
            session.commit()

    def convert_invocation_conversations(self, data):
        """ converts invocation dict to correct column names """
        clean_data = Conversations()

        clean_data.incident_id = data.incident_id
        clean_data.form = data.form
        clean_data.tweet_id = int(data.tweet_id)
        clean_data.in_reply_to_id = data.user_name

        return clean_data

    def convert_form_conversations(self, data):
        """ Converts form dict to correct column names """
        clean_data = Conversations()

        clean_data.form = 1
        clean_data.incident_id = data.incident_id
        clean_data.tweet_id = int(data.tweet_id)
        clean_data.root_tweet_city = data.city
        clean_data.root_tweet_state = data.state
        clean_data.root_tweet_lat = data.lat
        clean_data.root_tweet_long = data.long
        clean_data.root_tweet_date = data.incident_date
        clean_data.root_tweet_force_rank = data.force_rank
        clean_data.tweeter_id = data.user_name

        return clean_data

    def initialize_table(self, tablename):
        """ creates table if not exists and table model exists """

        if tablename in self.TABLE_NAMES:
            table = self.TABLE_NAMES[tablename]
        else:
            return "Table model not found"

        insp = inspect(self.engine)
        if not insp.has_table(tablename):
            table.__table__.create(self.engine)

    def reset_table(self, tablename):
        """ DANGER! this will delete all data in the table!!! """

        if tablename in self.TABLE_NAMES:
            table = self.TABLE_NAMES[tablename]
        else:
            return "Table model not found"

        check = input('Are you sure? This will delete all table data (Y/N):')
        if check == 'Y':
            insp = inspect(self.engine)
            if insp.has_table(tablename):
                table.__table__.drop(self.engine)
            self.initialize_table(tablename)
        elif check == 'N':
            pass
        else:
            print('You must answer Y or N to complete this function.')

    def drop_table(self, tablename):
        """ DANGER! this will delete the table!!! """

        if tablename in self.TABLE_NAMES:
            table = self.TABLE_NAMES[tablename]
        else:
            return "Table model not found"

        check = input('Are you sure? This will delete all table data (Y/N):')
        if check == 'Y':
            insp = inspect(self.engine)
            if insp.has_table(tablename):
                table.__table__.drop(self.engine)
        elif check == 'N':
            pass
        else:
            print('You must answer Y or N to complete this function.')

    def get_table(self, table_name, table_col_name=None, column_value=None):
        """
        This function will select tables based on the table name.
        This function is a helper function used to help in
        SQLAlchemy queries.
        """
        with self.Sessionmaker() as session:
            if column_value is not None:
                query = (select(table_name).where(
                    table_col_name == column_value))
                data = session.execute(query).fetchall()
                return data

            else:
                query = select(table_name)
                data = session.execute(query).fetchall()
                return data


    def insert_data(self, data):
        """
        Sets the active column for the given script_ID to False to deter the
        script from future use. Originally a "delete_script" function was
        conceived, but the potential need for more data on past script
        testing led to this function being employed instead.

        ----Labs 39 ---
        I suggest following our flow of creating helper function(s) in db.py to
        update 'bot_scripts' for the activate and deactivate functions.
        Then check endpoints in main.py to test this and set up the FE
        for connecting the modal in Admin dashboard.
        """
        # Update 'active' to True in 'bot_script' table for 'script_id'
        with self.Sessionmaker() as session: 
            session.add(data)
            session.commit()
