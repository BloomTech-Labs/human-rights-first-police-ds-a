import json
import os
from typing import Tuple, List, Dict

from dotenv import load_dotenv


from sqlalchemy import create_engine, select, insert, update, func, inspect
from sqlalchemy.orm import sessionmaker, scoped_session

from app.models import ForceRanks, Conversations #, Base


load_dotenv()
db_url = os.getenv('DB_URL')
#table_name = 'force_ranks'


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
            for datum in range(len(data)):
                last_value += 1
                data[datum]['incident_id'] = last_value
                if type(data[datum]['confidence']) != float:
                    data[datum]['confidence'] = data[datum]['confidence'].item()
                obj = ForceRanks(**data[datum])
                session.add(obj)
                session.commit()


    def insert_data_conversations(self, data: List[Dict]):
        """ inserts data into conversations """
        with self.Sessionmaker() as session:
            last = select(func.max(Conversations.id))
            last_value = session.execute(last).fetchall()[0][0]
            for datum in range(len(data)):
                last_value += 1
                data[datum]['id'] = last_value
                obj = Conversations(**data[datum])
                session.add(obj)
                session.commit()


    def update_force_rank(self, data, tweet_id):
        """ updates force rank columns of matching tweet_id """
        query = (
            update(ForceRanks).
            where(ForceRanks.tweet_id == str(tweet_id)).
            values(**data)
        )

        with self.Sessionmaker() as session:
            session.execute(query)
            session.commit()


    def update_conversations(self, data, tweet_id):
        """ updates conversations columns of matching tweet_id """
        query = (
            update(Conversations).
            where(Conversations.root_tweet_id == str(root_id)).
            values(**data)
        )

        with self.Sessionmaker() as session:
            session.execute(query)
            session.commit()


    def get_to_advance(self):
        """ gets highest conversation_status row of each root_tweet_id """
        with self.Sessionmaker() as session:
            query1 = select(
                func.max(Conversations.conversation_status).label("status"),
                Conversations.root_tweet_id
            ).group_by(
                Converstaions.root_tweet_id
            ).cte('wow')

            query2 = select(
                Conversations
            ).join(
                query1,
                query1.c.root_tweet_id == Conversations.root_tweet_id
            ).filter(
                Conversations.conversation_status == query1.c.status
            )

            data = session.execute(query2)

        return [i[0] for i in data.fetchall()]


    def update_conversation_checks(self, root_id):
        """ iterates conversation_checks column of matching root_tweet_id """
        query =(
            update(Conversations).
            where(Conversations.root_tweet_id == str(root_id)).
            values(checks_made = Conversations.checks_made + 1)
        )

        with self.Sessionmaker() as session:
            session.execute(query)
            session.commit()


    def initialize_ranks_table(self):
        """ creates force_ranks table if not exists """
        insp = inspect(self.engine)
        if insp.has_table("force_ranks") == False:
            ForceRanks.__table__.create(self.engine)


    def intialize_conversations_table(self):
        """ creates conversations table if not exists """
        insp = inspect(self.engine)
        if insp.has_table("conversations"):
            Conversations.__table__.create(self.engine)


    def reset_force_ranks(self):
        """ DANGER! this will delete all data in the table!!! """
        check = input('Are you sure? This will delete all table data (Y/N):')
        if check == 'Y':
            insp = inspect(self.engine)
            if insp.has_table("force_ranks") == True:
                ForceRanks.__table__.drop(self.engine)
            self.initialize_ranks_table()
        elif check == 'N':
            pass
        else:
            print('Please answer Y or N')


    def reset_conversations(self):
        """ DANGER! this will delete all data in the table!!! """
        check = input("Are you sure? This will delete all table data (Y/N):")
        if check == 'Y':
            insp = inspect(self.engine)
            if insp.has_table("conversations") == True:
                Conversations.__table__.drop(self.engine)
            self.initialize_conversations_table()
        elif check == 'N':
            pass
        else:
            print('Please answer Y or N')
