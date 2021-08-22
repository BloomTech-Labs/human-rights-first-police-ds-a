from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os

from app.db import Database
from app.franken_bert import FrankenBert
import psycopg2

DB = Database()

# Data with bad_usernames is all values 1332 < incident_id < 1962
# Need to insert a connection string
# Need to run from root directory (shouldn't need to run again, has already been applied)


#conn = psycopg2.connect('')

curs = conn.cursor()
curs.execute("SELECT incident_id, src FROM force_ranks WHERE incident_id > 1332 AND incident_id < 1962 ORDER BY incident_id")
results = curs.fetchall()
curs.close()
conn.close()


out = []
for i in results:
	ONE = i[0]
	TWO = i[1]
	TWO = TWO[22:].split('/')[0]
	out.append((TWO,ONE))

print(out)
#conn = psycopg2.connect('')


curs = conn.cursor()
for i in out:
	update = "UPDATE force_ranks SET user_name=%s WHERE incident_id=%s"
	val = i
	curs.execute(update, val)
	conn.commit()
curs.close()
conn.close()
