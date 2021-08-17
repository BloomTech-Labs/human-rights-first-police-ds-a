from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import json, os
from typing import Tuple, List, Dict

from sqlalchemy import create_engine, select, insert, update, func, inspect, and_
from sqlalchemy.orm import sessionmaker, scoped_session

from app.models import ForceRanks, Conversations

db_url = os.getenv('DB_URL2')

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


    def model_to_dict(self, obj):
        """ removes _sa_instance_state from .__dict__ representation of data model object """
        data = obj.__dict__
        if '_sa_instance_state' in data:
            del data['_sa_instance_state']

        return data


    def get_conversation_root(self, root_id: int):
        """ Get conversation with a specific tweet_id """
        with self.Sessionmaker() as session:
            query = select(Conversations).where(Conversations.tweet_id == root_id)
            conversations_data = session.execute(query)

        return [i[0] for i in conversations_data.fetchall()]


    def load_data_force_ranks(self):
        """ gets all data from force_ranks"""
        with self.Sessionmaker() as session:
            query = select(ForceRanks)
            force_ranks_data = session.execute(query).fetchall()

        return force_ranks_data


    def load_tweet_ids_force_ranks(self):
        """ gets all tweet_ids from force_ranks """
        with self.Sessionmaker() as session:
            query = select(ForceRanks.tweet_id)
            force_ranks_data = session.execute(query).fetchall()

        return force_ranks_data


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


    def insert_data_conversations(self, data: List[Dict]):
        """ inserts data into conversations """
        with self.Sessionmaker() as session:
            last = select(func.max(Conversations.id))
            last_value = session.execute(last).fetchall()[0][0]
            for i in range(len(data)):
                if last_value is None:
                    last_value = 0
                last_value += 1
                data[i]['id'] = last_value
                obj = Conversations(**data[i])
                session.add(obj)
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


    def get_root_seven(self, root_id):
        """ gets root_ids with value of 7 """
        with self.Sessionmaker() as session:
            query = (select(Conversations).
            filter(and_(Conversations.tweet_id == str(root_id), Conversations.conversation_status == 7)))
            check_data = session.execute(query)

        return check_data.fetchall()


    def get_sevens(self):
        """ get all conversations with value of 7 """
        with self.Sessionmaker() as session:
            query = (select(Conversations, ForceRanks).
            join(ForceRanks,
                and_(Conversations.tweet_id == ForceRanks.tweet_id, Conversations.conversation_status == 7)))
            data = session.execute(query).fetchall()

        out = []
        for i in data:
            record = {}
            record['tweet_id'] = i['Conversations'].tweet_id
            with self.Sessionmaker() as session:
                query = (select(ForceRanks).
                filter(ForceRanks.tweet_id == record['tweet_id']))
                point = session.execute(query).fetchall()
            record['city'] = i['Conversations'].root_tweet_city
            record['confidence'] = None
            record['description'] = i['ForceRanks'].description
            record['force_rank'] = i['Conversations'].root_tweet_force_rank
            record['incident_date'] = i['Conversations'].root_tweet_date
            record['incident_id'] = i['ForceRanks'].incident_id
            record['lat'] = i['Conversations'].root_tweet_lat
            record['long'] = i['Conversations'].root_tweet_long
            record['src'] = {e:i for (e,i) in enumerate(i['ForceRanks'].src.replace('"', '',).replace('[','').replace(']','').split(','))}
            record['state'] = i['Conversations'].root_tweet_state
            record['status'] = i['ForceRanks'].status
            record['tags'] = {e:i for (e,i) in enumerate(i['ForceRanks'].tags.replace('"', '',).replace('[','').replace(']','').split(','))}
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


    def convert_invocation_conversations(self, data):
        """ converts invocation dict to correct column names """
        clean_data = {}
        try:
            clean_data['form'] = data.form
        except KeyError:
            pass
        try:
            clean_data['isChecked'] = True
        except KeyError:
            pass
        try:
            clean_data['link'] = data.link
        except KeyError:
            pass
        try:
            clean_data['tweet_id'] = data.tweet_id
        except KeyError:
            pass
        try:
            clean_data['tweeter_id'] = data.user_name
        except KeyError:
            pass

        return clean_data


    def convert_form_conversations(self, data):
        """ Converts form dict to correct column names """
        clean_data = {}
        clean_data['form'] = 1
        try:
            clean_data['incident_id'] = data.incident_id
        except KeyError:
            pass
        try:
            clean_data['tweet_id'] = data.tweet_id
        except KeyError:
            pass
        try:
            clean_data['root_tweet_city'] = data.city
        except KeyError:
            pass
        try:
            clean_data['root_tweet_state'] = data.state
        except KeyError:
            pass
        try:
            clean_data['root_tweet_lat'] = data.lat
        except KeyError:
            pass
        try:
            clean_data['root_tweet_long'] = data.long
        except KeyError:
            pass
        try:
            clean_data['root_tweet_date'] = data.incident_date
        except KeyError:
            pass
        try:
            clean_data['root_tweet_force_rank'] = data.force_rank
        except KeyError:
            pass
        try:
            clean_data['tweeter_id'] = data.user_name
        except KeyError:
            pass

        return clean_data


    def initialize_table(self, tablename):
        """ creates table if not exists and table model exists """
        if tablename == 'force_ranks':
            table = ForceRanks
        elif tablename == 'conversations':
            table = Conversations
        else:
            return "Table model not found"

        insp = inspect(self.engine)
        if insp.has_table(tablename) == False:
            table.__table__.create(self.engine)


    def reset_table(self, tablename):
        """ DANGER! this will delete all data in the table!!! """
        if tablename == 'force_ranks':
            table = ForceRanks
        elif tablename == 'conversations':
            table = Conversations
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
            print('Please answer Y or N')
