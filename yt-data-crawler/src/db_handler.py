import os
import pprint
import datetime
import psycopg2
from psycopg2  import extras

DATABASE_URL = os.environ['DATABASE_URL']

def get_connection():
	# dsn = os.environ.get('DATABASE_URL')
	return psycopg2.connect(DATABASE_URL, sslmode='require')

def chan_record_gen(chan_data, main_category, sub_category):
	stat = chan_data['statistics']
	description = chan_data['snippet']['description']

	try:
		publish_data = chan_data['snippet']['publishedAt']
	except KeyError:
		print("can't get publishedAt")
		pprint.pprint(chan_data)
		publish_data = ''
	keywords = ''
	if 'keywords' in chan_data['brandingSettings']['channel']:
		keywords = chan_data['brandingSettings']['channel']['keywords']
	return (main_category, sub_category, chan_data['id'], chan_data['snippet']['title'], stat['viewCount'], stat['videoCount'], stat['subscriberCount'],
		chan_data['snippet']['thumbnails']['medium']['url'], description, keywords, chan_data['contentDetails']['relatedPlaylists']['uploads'],
		publish_data)

def video_record_gen(video_data, main_category, sub_category):
	channel_id = video_data['snippet']['channelId']
	channel_title = video_data['snippet']['channelTitle']
	video_id = video_data['id']
	video_title = video_data['snippet']['title']
	description = video_data['snippet']['description']
	published_at = video_data['snippet']['publishedAt']
	thumbnail = video_data['snippet']['thumbnails']['medium']['url']
	view_count = 0
	like_count = 0
	if 'likeCount' in video_data['statistics']:
		like_count = video_data['statistics']['likeCount']
	if 'viewCount' in video_data['statistics']:
		view_count = video_data['statistics']['viewCount']

	return (main_category, sub_category, channel_id, channel_title, video_id, video_title, view_count,
		like_count, thumbnail, description, published_at)

def check_should_update(conn, cur, mod, name):
	cur.execute('SELECT * FROM update_info WHERE name = %s', (name,))
	row = cur.fetchone()
	count = 0
	if row is not None:
		count = int(row['count'])
	cur.execute('DELETE FROM update_info  WHERE name = %s', (name,))
	date = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
	cur.execute('INSERT INTO update_info VALUES (%s, %s, %s)', (date, str(count + 1), name))
	conn.commit()
	return count%mod == 0

def print_channel_row(channel_id,table_name, cur):
	cur.execute('SELECT * FROM channel WHERE channel_id = %s', (channel_id,))
	print(cur.fetchone()[3])

def get_channel_from_id(channel_id, cur):
	cur.execute('SELECT * FROM channel WHERE channel_id = %s', (channel_id,))
	return cur.fetchall()

def get_video_from_channel_id(channel_id, cur):
	cur.execute('SELECT * FROM video WHERE channel_id = %s', (channel_id,))
	return cur.fetchone()

def delete_channel(channel_id, cur):
	cur.execute('DELETE FROM channel WHERE channel_id = %s', (channel_id,))

def delete_video(channel_id, cur):
	cur.execute('DELETE FROM video WHERE channel_id = %s', (channel_id,))

def is_exist_channel(channel_id, cur):
	cur.execute('SELECT EXISTS(SELECT * FROM channel WHERE channel_id = %s)', (channel_id,))
	return cur.fetchone()[0]

def add_data(records, table_name):
	with get_connection() as conn:
		with conn.cursor() as cur:
			extras.execute_values(cur, 'INSERT INTO ' + table_name + ' VALUES %s', records)
			conn.commit()

def add_data_with_conn(records, table_name, conn, cur):
		extras.execute_values(cur, 'INSERT INTO  ' + table_name + ' VALUES %s', records)
		conn.commit()
