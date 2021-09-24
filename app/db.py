"""
This module should should hold everything related to the database including:
- Connections
- Queries
And now Bot Scripts
"""

from dotenv import load_dotenv, find_dotenv
from random import random as rand
import os

from sqlalchemy.ext.declarative import declarative_base
""" Find documentation for declaritive base here:
https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base
"""
from sqlalchemy import create_engine, inspect, select, update, func, and_
from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey

from typing import List, Dict

from sqlalchemy.orm import relationship, sessionmaker, scoped_session
""" Find documentation for sessions here:
https://docs.sqlalchemy.org/en/14/orm/session_basics.html#using-a-sessionmaker
AND
https://docs.sqlalchemy.org/en/14/orm/contextual.html
"""

load_dotenv(find_dotenv())

db_url = os.getenv("DB_URL")

engine = create_engine(db_url, echo=True)  # create connection to the database to perform SQL operations, echo will generate the activity log

Base = declarative_base()  # describes db tables and then defines classes that will be mapped to those tables


class ForceRanks(Base):
    """
    Describe the Postgres tables AND
    Map a path to those tables
    Documentation for Base:
    https://tinyurl.com/ac5tf34w
    """
    __tablename__ = "force_ranks"  # name formatting has to be this way

    incident_id = Column(Integer, primary_key=True, nullable=False, unique=True)
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


class Training(Base):
    __tablename__ = "training"

    id = Column(Integer, primary_key=True)
    tweets = Column(String)
    labels = Column(Integer)
    
    def __repr__(self):
        return(
			"id:{}, tweets:{}, labels:{}").format(
			self.id,
			self.tweets,
			self.labels
			)


class BotScripts(Base):

    __tablename__ = "bot_scripts"

    script_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    script = Column(String(255))
    convo_node = Column(Integer)
    use_count = Column(Integer)
    positive_count = Column(Integer)
    success_rate = Column(Float)
    active = Column(Boolean)

    def __repr__(self):
        return (
            "script_id:{}, script:{}, convo_node:{}, use_count:{}, positive_count:{}, success_rate{}, active:{}").format(
            self.script_id,
            self.script,
            self.convo_node,
            self.use_count,
            self.positive_count,
            self.success_rate,
            self.active
            )


class ScriptTesting(Base):

	__tablename__ = "script_testing"

	incident_id = Column(Integer, primary_key=True, nullable=False, unique=True)
	script_path = Column(String(100))
	success = Column(Boolean)

	
	def __repr__(self):
		return (
			"incident_id:{}, script_path:{}, success:{}").format(
			self.incident_id,
			self.script_path,
			self.success
			)


class Sources(Base):

	__tablename__ = "sources"

	source_id = Column(Integer, primary_key=True, nullable=False, unique=True)
	incident_id = Column(Integer, ForeignKey("force_ranks.incident_id"))
	source = Column(String(255))

	
	def __repr__(self):
		return (
			"source_id:{}, incident_id:{}, sources:{}").format(
			self.source_id,
			self.incident_id,
			self.source
			)


class Tags(Base):

	__tablename__ = "tags"

	tags_id = Column(Integer, primary_key=True, nullable=False, unique=True)
	incident_id = Column(Integer, ForeignKey("force_ranks.incident_id"))
	tag = Column(String(40))

	
	def __repr__(self):
		return (
			"tags_id:{}, incident_id:{}, sources:{}").format(
			self.tags_id,
			self.incident_id,
			self.tag
			)


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
                            "bot_scripts": BotScripts,
                            "script_testing": ScriptTesting,
                            "tags": Tags,
                            "sources": Sources
                            }


    def model_to_dict(self, obj):
        """ removes _sa_instance_state from .__dict__ representation of data model object """
        data = obj.__dict__
        if '_sa_instance_state' in data:
            del data['_sa_instance_state']

        return data

    def get_conversation_root(self, root_id: int):
        """ Get conversation with a specific root_tweet_id """
        with self.Sessionmaker() as session:
            query = select(Conversations).where(Conversations.tweet_id == root_id)
            conversations_data = session.execute(query)

        return [i[0] for i in conversations_data.fetchall()]


    def get_script_ids(self, convo_node):
        """
        Gets the script_ids associated with the given convo_node 
        ONLY KEPT FOR FUTURE USE.
        This funtion can be replaced with get_table().
        """
        with self.Sessionmaker() as session:
            query = (
                select(BotScripts.script_id).
                where(BotScripts.convo_node == convo_node))
            script_ids_data = session.execute(query).fetchall()

        return script_ids_data


    def get_script(self, script_id):
        """ 
        Gets a script from 'bot_scripts' table for given script_id(s)
        ONLY KEPT FOR FUTURE USE.
        This funtion can be replaced with get_table(). 
        """
        with self.Sessionmaker() as session:
            query = (
                select(BotScripts.script).
                where(BotScripts.script_id == script_id)
                )

            script_data = session.execute(query).fetchall()

        return script_data


    def get_all_script_data(self):
        """
        ONLY KEPT FOR FUTURE USE.
        This funtion can be replaced with get_table().
        Selects all from 'bot_scripts'
        
        ---Labs 38 ---> you may need to tailor the output type here for populating
        the Script Management modal, consult you front end peeps

        https://whimsical.com/script-selection-2xBPsVkfFyfdjMTPQVUHfQ
        """
        with self.Sessionmaker() as session:
            query = select(BotScripts)
            bot_scripts_data = session.execute(query).fetchall()

        return bot_scripts_data


    def insert_script(self, new_script):
        """
        Updates the bot_scripts table with new row passing the given script
        and indicated conversation node into their respective columns. Sets the
        'use_count' and 'positive_count' columns for this row to the default of 0.
        'active' column set to True by default. Generates a new 'script_ID' unique
        to this script.
        """

        with self.Sessionmaker() as session:
            BS = BotScripts()
            BS.script_id = new_script.script_id
            BS.script = new_script.script
            BS.convo_node = new_script.convo_node
            BS.use_count = new_script.use_count
            BS.positive_count = new_script.positive_count
            BS.success_rate = new_script.success_rate
            BS.active = new_script.active
            session.add(BS)
            session.commit()


    def get_use_count(self, script_id):
        """ 
        Gets the use_count from 'bot_scripts' for given script_id
        ONLY KEPT FOR FUTURE USE.
        This funtion can be replaced with get_table(). 
        """
        with self.Sessionmaker() as session:
            query = (
                select(BotScripts.use_count).
                where(BotScripts.script_id == script_id)
            )

            use_count = session.execute(query).fetchall()

        return use_count


    def get_counts(self, script_id):
        """
        Gets use_count and positive_count from 'bot_scripts' given script_id 
        """
        with self.Sessionmaker() as session:
            query = (
                select(BotScripts.use_count, BotScripts.positive_count).
                where(BotScripts.script_id == script_id)
            )

            counts = session.execute(query).fetchall()

        return counts
    

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
                       ).
                where(BotScripts.convo_node == convo_node)
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
            query = (
                    update(BotScripts).
                    where(BotScripts.script_id == script_id).
                    values(**data)
                )

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
                if type(data[i]['confidence']) != float and data[i]['confidence'] != None:
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
        query = (
            update(table).
            where(table.tweet_id == str(tweet_id)).
            values(**data)
        )

        with self.Sessionmaker() as session:
            session.execute(query)
            session.commit()


    def get_root_twelve(self, root_id):
        """ gets root_ids with value of 12 """
        with self.Sessionmaker() as session:
            query = (select(Conversations).
            filter(and_(Conversations.tweet_id == str(root_id), Conversations.conversation_status == 12)))
            check_data = session.execute(query)

        return check_data.fetchall()


    def get_twelves(self):
        """ get all conversations with value of 12 and corresponding data from force_ranks """
        with self.Sessionmaker() as session:
            query = (select(Conversations, ForceRanks).
            join(ForceRanks,
                and_(Conversations.tweet_id == ForceRanks.tweet_id, Conversations.conversation_status == 12)))
            data = session.execute(query).fetchall()

        out = []
        for i in data:
            record = {}
            record['tweet_id'] = i['Conversations'].tweet_id
            record['city'] = i['Conversations'].root_tweet_city
            record['confidence'] = None
            record['description'] = i['ForceRanks'].description
            record['force_rank'] = i['Conversations'].root_tweet_force_rank
            record['incident_date'] = i['Conversations'].root_tweet_date
            record['incident_id'] = i['ForceRanks'].incident_id
            record['lat'] = i['Conversations'].root_tweet_lat
            record['long'] = i['Conversations'].root_tweet_long
            try:
                record['src'] = {e:i for (e,i) in enumerate(i['ForceRanks'].src.replace('"', '',).replace('[','').replace(']','').split(','))}
            except (KeyError, AttributeError):
                pass
            record['state'] = i['Conversations'].root_tweet_state
            record['status'] = i['ForceRanks'].status
            try:
                record['tags'] = {e:i for (e,i) in enumerate(i['ForceRanks'].tags.replace('"', '',).replace('[','').replace(']','').split(','))}
            except (KeyError, AttributeError):
                pass
            print(i['ForceRanks'].tags)
            record['title'] = i['ForceRanks'].title
            record['user_name'] = i['ForceRanks'].user_name
            out.append(record)

        return out


    def get_user_name(self):
        """ gets user_name from src """
        with self.Sessionmaker() as session:
            query = (select(ForceRanks).
                filter(ForceRanks.incident_id > 1332).
                order_by(ForceRanks.incident_id.desc())

                )
            data = session.execute(query).fetchall()
            for datum in data:
                if datum['ForceRanks'].src[:22] == '["https://twitter.com/': # REEEMOVE FOR PROD
                    point = datum[0].src[22:]
                    point = point[:point.index('/')]
                    datum['ForceRanks'].user_name = point

        return data


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
        query =(
            update(Conversations).
            where(Conversations.tweet_id == str(root_id)).
            values(checks_made = Conversations.checks_made + 1)
        )

        with self.Sessionmaker() as session:
            session.execute(query)
            session.commit()


    def convert_invocation_conversations(self, data):  # TODO Refactor 
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
        if insp.has_table(tablename) == False:
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
            if insp.has_table(tablename) == True:
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
            if insp.has_table(tablename) == True:
                table.__table__.drop(self.engine)
        elif check == 'N':
            pass
        else:
            print('You must answer Y or N to complete this function.')
            

    def get_table(self, table_name, table_col_name = None, column_value = None):
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
                query = (select(table_name))
                data = session.execute(query).fetchall()
                return data


class ScriptMaster():
    """Tools for modifying 'bot_scripts' table and script selection"""

    def __init__(self):
        self.convo_node_dict = {0: "welcome",  #needs revision when nodes are reworked
                                10: "DM permission",
                                11: "form invitation"
                                }

    def add_script(self, data):
        """
        Updates the bot_scripts table with new row passing the given script
        and indicated conversation node into their respective columns. Sets the
        'use_count' and 'positive_count' columns for this row to the default of 0,
        'success_rate' column defaults to 0.0, and 'active' defaults True.
        Auto generates a new 'script_ID' incrementally for scripts all
        conversation nodes except 'welcome' which will need to use a helper
        function which authenticates the welcome message with Twitter and generates
        a different ID.
        """

        if data.script_id != 0:
            # data['script_id'] =  # Use id from Twitter auth function (to be written or grabbed from Brody O.)
            pass
        else:
            # data['script_id'] = # Auto generate the next incremental id
            pass

        # Database.insert_script(data)

    def deactivate_script(script_ID):
        """
        Sets the active column for the given script_ID to False to deter the script
        from future use. Originally a "delete_script" function was conceived, but
        the potential need for more data on past script testing led to this
        function being employed instead.

        ----Labs 38 ---
        I suggest following our flow of creating helper function(s) in db.py to 
        update 'bot_scripts' for the activate and deactivate functions.
        Then check endpoints in main.py to test this and set up the FE for connecting
        the modal in Admin dashboard.
        """

        # Update 'active' to False in 'bot_script' table for 'script_id'
        pass

    def activate_script(script_ID):
        # Update 'active' to True in 'bot_script' table for 'script_id'
        pass

    def add_to_use_count(script_id):
        """
        Uses functions from db.py as helper to increment the use_count
        """
        old_count = Database.get_table(BotScripts.use_count,BotScripts.script_id, script_id)
        print(old_count)
        new_count = old_count[0][0] + 1
        Database.bump_use_count(script_id, new_count)

    def add_to_positive_count(script_id):
        """
        Uses functions from db.py as helper to increment the positive_count
        """
        data = Database.get_counts(script_id)
        use = data[0][0]
        pos = data[0][1]

        pos += 1
        rate = pos / use
        Database.update_pos_and_success(script_id, pos, rate)

    # Functions for selection of scripts
    """ FUTURE update: add randomized functionality to choose between path-based
    script selection based on traning from the 'script_training' and 
    path-generating options (the latter exist below). Possibly set this up to occur
    automatically whence results from traing sessions of path-based data are available.

    Also consider setting up testing to occur automatically whence
    sufficient training data becomes available. Also consider scheduling automatic
    training per a given number of data points received thereafter. Reccomend having
    said training take place on another optional instance (with the bot sentiment
    analysis) as memory on current instance is running low.
    """

    def choose_script(self, status):
        """
        Used to select a script for use by the twitter bot given a conversation node.
        Returns a tuple containing the script and its id to be used by the Twitter bot.
        The script for the conversation and the script_id to be used in another two
        function calls within the bot to update the use_count in 'bot_scripts' when
        the bot send the message as well as updating the path in 'script_testing' after
        the bot pairs this script_id with an incident_id.
        
        -----
        In a future implementation try switching between choosing a random script and 
        choosing the better of two as originally coded.
        -----

        """

        # Pull the list of scripts for a convo_node given
        script_data = Database.get_scripts_per_node(self.convo_node_dict[status])

        # Randomly select two script objects
        l = len(script_data)
        x = int(str(rand())[-6:])
        y = int(str(rand())[-6:])
        a = x % l
        b = y % l

        # Make conditional for selecting the best of two if use counts are high enough
        if script_data[a][2] > 100 and script_data[b][2] > 100:
            if script_data[a][3] >= script_data[b][3]:
                use = a
            else:
                use = b
        else:
            if x >= y:
                use = a
            else:
                use = b
        
        return (script_data[use][0], script_data[use][1])