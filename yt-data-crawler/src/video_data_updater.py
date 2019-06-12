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

def update_video_data(conn, cur, channel_id, uplist_id, main_category, sub_category):
	old = db.get_video_from_channel_id(channel_id, cur)
	old_vid = None
	if old is not None:
		old_vid = old['video_id']

	db.delete_video(channel_id, cur)
	video_data = ytapi.get_latest_video_data(uplist_id, 2)

	if video_data is None:
		print("Cound not get video data")
		return

	if check_pubulish_date(video_data['snippet']['publishedAt'], 1):
		print("get new video")
		ret = {'vid' : None}
		if old_vid is None or old_vid != video_data['id']:
			ret['vid'] = video_data['id']
			print("bland new")

		row = [db.video_record_gen(video_data, main_category, sub_category)]
		db.add_data_with_conn(row, 'video', conn, cur)
		return ret

	return None

def check_pubulish_date(published_date, span):
	date = published_date.split('T')[0].split('-')
	published_date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
	deadline = datetime.date.today() - datetime.timedelta(weeks = span)
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
		cur.execute('SELECT * FROM channel')
		rows = cur.fetchall()
		for (id, row) in enumerate(rows):
			print(row['channel_title'])
			ret = update_video_data(conn, cur, row['channel_id'], row['uploads_id'],
				row['main_category'], row['sub_category'])
			if ret is not None:
				if row['main_category'] in video_sums:
					video_sums[row['main_category']] += 1
				else :
					video_sums[row['main_category']] = 0
				if ret['vid'] is not None:
					new_video_info.append({'video_id': ret['vid'],
					'channel_title': row['channel_title'], 'category': row['main_category'] })
		tweets = []
		tw_new_video = '{}さんの新しい動画。  https://www.youtube.com/watch?v={} https://ytchan.herokuapp.com/{}/video #{}'
		tw_text = '最近の動画を更新しました。 カテゴリ->{}  動画数->{} https://ytchan.herokuapp.com/{}/video #Youtube #{}'
		for category, value in video_sums.items():
			category_encoded = urllib.parse.urlencode({'q' : category})[2:]
			tweets.append(tw_text.format(category, value ,category_encoded, category))
			print("%s %d" % (category, value))
		for video in new_video_info:
			category_encoded = urllib.parse.urlencode({'q' : video['category']})[2:]
			tweets.append(tw_new_video.format(video['channel_title'], video['video_id'], category_encoded,
				video['category']))
		tw.tweet_mul(cur, tweets)