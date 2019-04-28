import os
import psycopg2
from psycopg2  import extras

DATABASE_URL = os.environ['DATABASE_URL']

def get_connection():
	# dsn = os.environ.get('DATABASE_URL')
	return psycopg2.connect(DATABASE_URL, sslmode='require')

def add_channel_to_db(chan_data, table_name, conn, cur):
	# chandata (category, subCategory, channelId, channelTitle, channelType, viewCount, videoCount, subscriberCount, thumbnail_url )
	if not is_exist_channel(chan_data[0][2], table_name, conn, cur):
		extras.execute_values(cur, 'INSERT INTO  ' + table_name + ' VALUES %s', chan_data)
		conn.commit()

def add_channels_to_db(chan_data, table_name, conn, cur):
	extras.execute_values(cur, 'INSERT INTO  ' + table_name + ' VALUES %s', chan_data)
	conn.commit()

def is_exist_channel(channel_id,table_name, conn, cur):
	cur.execute('SELECT EXISTS(SELECT * FROM channel WHERE channelid = %s)', (channel_id,))
	return cur.fetchone()[0]

def add_channels(chan_data, table_name):
	with get_connection() as conn:
		with conn.cursor() as cur:
			add_channels_to_db(chan_data, table_name, conn, cur)

def add_channel(chan_data, table_name):
	with get_connection() as conn:
		with conn.cursor() as cur:
			add_channel_to_db(chan_data, table_name, conn, cur)