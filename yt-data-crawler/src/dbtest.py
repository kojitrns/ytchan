import os
import psycopg2
from psycopg2  import extras

DATABASE_URL = os.environ['DATABASE_URL']

def get_connection():
	# dsn = os.environ.get('DATABASE_URL')
	return psycopg2.connect(DATABASE_URL, sslmode='require')

def add_chan_to_db(chan_data, table_name, conn, cur):
	# chandata (category, subCategory, channelId, channelTitle, channelType, viewCount, videoCount, subscriberCount, thumbnail_url )
	extras.execute_values(cur, 'INSERT INTO  ' + table_name + ' VALUES %s', chan_data)
	conn.commit()

def test_add_chan(chan_data, table_name):
	with get_connection() as conn:
		with conn.cursor() as cur:
			add_chan_to_db(chan_data, table_name, conn, cur)