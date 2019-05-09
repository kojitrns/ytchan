import os
import pprint
import psycopg2
from psycopg2  import extras

DATABASE_URL = os.environ['DATABASE_URL']

def get_connection():
	# dsn = os.environ.get('DATABASE_URL')
	return psycopg2.connect(DATABASE_URL, sslmode='require')

def chan_record_gen(chan_data, main_category, sub_category):
	stat = chan_data['statistics']
	description = chan_data['snippet']['description']
	publish_data = chan_data['snippet']['publishedAt']
	keywords = ''
	if 'keywords' in chan_data['brandingSettings']['channel']:
		keywords = chan_data['brandingSettings']['channel']['keywords']
	return (main_category, sub_category, chan_data['id'], chan_data['snippet']['title'], stat['viewCount'], stat['videoCount'], stat['subscriberCount'],
		chan_data['snippet']['thumbnails']['medium']['url'], description, keywords, chan_data['contentDetails']['relatedPlaylists']['uploads'],
		publish_data)

def print_channel_row(channel_id,table_name, cur):
	cur.execute('SELECT * FROM channel WHERE channelid = %s', (channel_id,))
	print(cur.fetchone()[3])

def delete_channel(channel_id, cur):
	cur.execute('DELETE FROM channel WHERE channelid = %s', (channel_id,))

def update_channel(channel_id, uplist_id, cur):
	cur.execute('UPDATE channel SET uploads_list_id = %s WHERE channelid = %s;', (uplist_id, channel_id,))

def add_channels_to_db(chan_data, table_name, conn, cur):
	extras.execute_values(cur, 'INSERT INTO  ' + table_name + ' VALUES %s', chan_data)
	conn.commit()

def is_exist_channel(channel_id,table_name, cur):
	cur.execute('SELECT EXISTS(SELECT * FROM channel WHERE channelid = %s)', (channel_id,))
	return cur.fetchone()[0]

def add_channels(chan_data, table_name):
	with get_connection() as conn:
		with conn.cursor() as cur:
			add_channels_to_db(chan_data, table_name, conn, cur)
