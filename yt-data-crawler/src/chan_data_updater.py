# coding: utf-8
import pprint
import db_handler as db
import api_handler as ytapi

ROW_CONTENTS = ['main_category','sub_category','channel_id','title','viewCount','videoCount','subscriberCount',
'thumbnail_url','description','keywords','uploads_id', 'publishe_date']

DATA_ROW_MAPPING = {}

def init():
	for (id , content) in enumerate(ROW_CONTENTS):
		DATA_ROW_MAPPING[content] = id
	pprint.pprint(DATA_ROW_MAPPING)

def update_channel_data(conn, cur, channel_id, main_category, sub_category):
	db.delete_channel(channel_id, cur)
	chan_data = ytapi.get_channel_data(channel_id, 3)
	if chan_data is None:
		print("Cound not get chan data")
		return

	row = [db.chan_record_gen(chan_data, main_category, sub_category)]
	db.add_data_with_conn(row, 'channel', conn, cur)

def is_valid_channel(chan_data):
	return chan_data[DATA_ROW_MAPPING['viewCount']] > 0

init()

with db.get_connection() as conn:
	with conn.cursor() as cur:
		cur.execute('SELECT * FROM channel')
		rows = cur.fetchall()
		for (id, row) in enumerate(rows):
			if is_valid_channel(row):
				update_channel_data(conn,cur,row[DATA_ROW_MAPPING['channel_id']],row[DATA_ROW_MAPPING['main_category']],row[DATA_ROW_MAPPING['sub_category']])
			else:
				db.delete_channel(row[DATA_ROW_MAPPING['channel_id']], cur)
				print("delete")
			print("%d %s %s %s" % (id, row[DATA_ROW_MAPPING['title']],row[DATA_ROW_MAPPING['main_category']],row[DATA_ROW_MAPPING['sub_category']]))
