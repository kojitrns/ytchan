import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

def get_connection():
	# dsn = os.environ.get('DATABASE_URL')
	return psycopg2.connect(DATABASE_URL, sslmode='require')

def add_chan_to_db(chan_data, table_name, conn, cur):
	# chandata (channelId, channelTitle, channelType, viewCount, videoCount, subscriberCount, thumbnail_url )
	cur.execute('INSERT INTO  '+table_name+' VALUES (%s, %s, %s, %s, %s, %s, %s)', chan_data)
	conn.commit()

def test_add_chan(chan_data):
	with get_connection() as conn:
		with conn.cursor() as cur:
			add_chan_to_db(chan_data, 'youtubers', conn, cur)
		conn.commit()
