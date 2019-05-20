# coding: utf-8
import pprint
import time
import datetime
import db_handler as db
import api_handler as ytapi

ROW_CONTENTS = ['main_category','sub_category','channel_id','title','viewCount','videoCount','subscriberCount',
'thumbnail_url','description','keywords','uploads_id', 'publishe_date']

DATA_ROW_MAPPING = {}

def init():
	for (id , content) in enumerate(ROW_CONTENTS):
		DATA_ROW_MAPPING[content] = id
	pprint.pprint(DATA_ROW_MAPPING)

def update_video_data(conn, cur, channel_id, uplist_id, main_category, sub_category):
	db.delete_video(channel_id, cur)
	video_data = ytapi.get_latest_video_data(uplist_id)
	if video_data is None:
		print("retry")
		time.sleep(5)
		video_data = ytapi.get_latest_video_data(uplist_id)
		if video_data is None:
			print("cant get")
			return
	if check_pubulish_date(video_data['snippet']['publishedAt'], 1):
		row = [db.video_record_gen(video_data, main_category, sub_category)]
		db.add_data_with_conn(row, 'video', conn, cur)

def is_valid_channel(chan_data):
	return chan_data[DATA_ROW_MAPPING['viewCount']] > 0

def check_pubulish_date(published_date, span):
	date = published_date.split('T')[0].split('-')
	published_date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
	deadline = datetime.date.today() - datetime.timedelta(weeks = span)
	print(deadline)
	print(published_date)
	return deadline < published_date

init()

with db.get_connection() as conn:
	with conn.cursor() as cur:
		cur.execute('SELECT * FROM channel')
		rows = cur.fetchall()
		for (id, row) in enumerate(rows):
			if is_valid_channel(row):
				print(row[DATA_ROW_MAPPING['title']])
				update_video_data(conn, cur, row[DATA_ROW_MAPPING['channel_id']], row[DATA_ROW_MAPPING['uploads_id']],
					row[DATA_ROW_MAPPING['main_category']], row[DATA_ROW_MAPPING['sub_category']])
