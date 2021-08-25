from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os

from app.db import Database
from app.franken_bert import FrankenBert
import psycopg2

DB = Database()

# Data from PB2020 is all values 6 < incident_id < 1333
# Need to insert a connection string
# Need to run from root directory (shouldn't need to run again, has already been applied)

#conn = psycopg2.connect('')

curs = conn.cursor()
curs.execute("SELECT incident_id, incident_date FROM force_ranks")
results = curs.fetchall()
curs.close()
conn.close()

print(results)
print(len(results))

out = []
for i in results:
	if i[0] > 6 and i[0] < 1333:
		row = (i[1].split('T')[0], i[0])
	else:
		row = (i[1].split(' ')[0], i[0])
	out.append(row)

print(out)
print(len(out))


# conn = psycopg2.connect('')

curs = conn.cursor()
for i in out:
	update = "UPDATE force_ranks SET incident_date=%s WHERE incident_id=%s"
	val = i
	curs.execute(update, val)
	conn.commit()
curs.close()
conn.close()
