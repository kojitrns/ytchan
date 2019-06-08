# coding: utf-8
import pprint
import sys
import time
import datetime
import db_handler as db
import api_handler as ytapi

ROW_CONTENTS = ['main_category','sub_category','channel_id','title','viewCount','videoCount','subscriberCount',
'thumbnail_url','description','keywords','uploads_id', 'publishe_date']


# def init():

def update_video_data(conn, cur, channel_id, uplist_id, main_category, sub_category):
	db.delete_video(channel_id, cur)
	video_data = ytapi.get_latest_video_data(uplist_id, 2)
	if video_data is None:
		print("Cound not get video data")
		return

	if check_pubulish_date(video_data['snippet']['publishedAt'], 1):
		print("get new video")
		row = [db.video_record_gen(video_data, main_category, sub_category)]
		db.add_data_with_conn(row, 'video', conn, cur)


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

		cur.execute('SELECT * FROM channel')
		rows = cur.fetchall()
		for (id, row) in enumerate(rows):
			print(row['channel_title'])
			update_video_data(conn, cur, row['channel_id'], row['uploads_id'],
				row['main_category'], row['sub_category'])