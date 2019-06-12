# coding: utf-8
import pprint
import sys
import time
import urllib
import datetime
import db_handler as db
import api_handler as ytapi
from twitter import tw_handler as tw

ROW_CONTENTS = ['main_category','sub_category','channel_id','title','viewCount','videoCount','subscriberCount',
'thumbnail_url','description','keywords','uploads_id', 'publishe_date']

# def init():

def bland_new_check(conn, cur, channel_id, uplist_id, main_category, sub_category):
	old = db.get_video_from_channel_id(channel_id, cur)
	old_vid = None
	if old is None:
		return False

	if check_pubulish_date(old['published_at'], 2):
		return old['video_id']

	return False

def check_pubulish_date(published_date, span_dasy):
	print(published_date)
	date = published_date.split('T')[0].split('-')
	published_date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
	deadline = datetime.date.today() - datetime.timedelta(days = span_dasy)
	return deadline < published_date

# init()

with db.get_connection() as conn:
	with conn.cursor(cursor_factory = db.psycopg2.extras.DictCursor) as cur:
		if len(sys.argv) > 1:
			print(sys.argv)
			cur.execute('SELECT * FROM channel WHERE channelid = %s', (sys.argv[1],))
			row = cur.fetchone()
			print(row['channeltitle'])
			print(row['uploads_id'])
			update_video_data(conn, cur, row['channel_id'], row['uploads_id'],
				row['main_category'], row['sub_category'])
			exit()

		video_sums = {}
		new_video_info = []
		bland_news = 0
		cur.execute('SELECT * FROM channel')
		rows = cur.fetchall()
		for (id, row) in enumerate(rows):
				print(row['channel_title'])
				ret = bland_new_check(conn, cur, row['channel_id'], row['uploads_id'],
				row['main_category'], row['sub_category'])
				if ret :
					new_video_info.append({'video_id': ret,
					'channel_title': row['channel_title'], 'category': row['main_category'] })
				print("")
		tweets = []
		tw_new_video = '{}さんの新しい動画。https://www.youtube.com/watch?v={} https://ytchan.herokuapp.com/{}/video #{}'

		print(bland_news)
		for video in new_video_info:
			print("bland new chan %s %s %s" % (video['channel_title'], video['video_id'], video['category']))
		for video in new_video_info:
			category_encoded = urllib.parse.urlencode({'q' : video['category']})[2:]
			tweets.append(tw_new_video.format(video['channel_title'], video['video_id'], category_encoded,
				video['category']))
		tw.tweet_mul(cur, tweets)