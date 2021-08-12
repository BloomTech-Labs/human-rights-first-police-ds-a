import json
import os
from typing import Tuple, List, Dict

from dotenv import load_dotenv
import psycopg2

from sqlalchemy import create_engine, select, insert, update, func, inspect
from sqlalchemy.orm import sessionmaker, scoped_session

from app.models import ForceRanks, Base

load_dotenv()
db_url = os.getenv('DB_URL')
table_name = 'force_ranks'


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

        data = obj.__dict__
        if '_sa_instance_state' in data:
            del data['_sa_instance_state']

        return data


    def load_data(self):

        with self.Sessionmaker() as session:
            query = select(ForceRanks)
            force_ranks_data = force_ranks_data = session.execute(query).fetchall()


        return force_ranks_data


    def insert_data(self, data: List[Dict]):

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


    def initialize_ranks_table(self):
        insp = inspect(self.engine)
        if insp.has_table(table_name) == False:
            ForceRanks.__table__.create(self.engine)


    def reset_table(self):
        """ DANGER! this will delete all data in the table!!! """
        insp = inspect(self.engine)
        if insp.has_table(table_name) == True:
            ForceRanks.__table__.drop(self.engine)
        self.initialize_ranks_table()

