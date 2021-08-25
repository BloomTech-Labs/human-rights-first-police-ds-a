from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os

from app.db import Database
from app.franken_bert import FrankenBert
import psycopg2

#########################################################
# Data from PB2020 is all values 6 < incident_id < 1333 #
# needs to be run from root of directory                #
# Needs a connection string                             #
#########################################################

DB = Database()

model = FrankenBert("app/saved_model")

#conn = psycopg2.connect('')

curs = conn.cursor()
curs.execute("SELECT incident_id, description FROM force_ranks WHERE confidence IS Null")
results = curs.fetchall()
curs.close()
conn.close()

print(results)
print(len(results))

lookup = {
    0: "Rank 0",
    1: "Rank 1",
    2: "Rank 2",
    3: "Rank 3",
    4: "Rank 4",
    5: "Rank 5",
}

out = []
wonky = []
for i in results:

	ONE = i[0]
	rank, conf = model.predict(i[1])
	s_rank = lookup[rank]
	TWO = s_rank
	THREE = conf.item()
	out.append((TWO, THREE, ONE))
	wonky.append(ONE)
print(out)


#conn = psycopg2.connect('')

curs = conn.cursor()
for i in out:
	update = "UPDATE force_ranks SET force_rank=%s, confidence=%s WHERE incident_id=%s"
	val = i
	curs.execute(update, val)
	conn.commit()
curs.close()
conn.close()
