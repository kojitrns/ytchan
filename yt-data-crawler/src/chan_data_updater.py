# coding: utf-8
import pprint
import db_handler as db
import api_handler as ytapi

ROW_CONTENTS = ['main_category','sub_category','channel_id','title','viewCount','videoCount','subscriberCount',
'thumbnail_url','description','keywords','uploads_id', 'publishe_date']

dup_list = []

# def init():

def update_channel_data(conn, cur, channel_id):
	channels = db.get_channel_from_id(channel_id, cur)
	if len(channels) > 1:
		dup_list.append(channel_id)
		
	db.delete_channel(channel_id, cur)

	chan_data = ytapi.get_channel_data(channel_id, 2)
	if chan_data is None:
		print("Cound not get chan data")
		return

	for old_data in channels:
		row = [db.chan_record_gen(chan_data, old_data['maincategory'], old_data['subcategory'])]
		db.add_data_with_conn(row, 'channel', conn, cur)


def is_valid_channel(chan_data):
	return chan_data['viewcount'] > 0

# init()

with db.get_connection() as conn:
	with conn.cursor(cursor_factory = db.psycopg2.extras.DictCursor) as cur:
		cur.execute('SELECT * FROM channel')
		rows = cur.fetchall()
		for (id, row) in enumerate(rows):
			if is_valid_channel(row):
				if not row['channelid'] in dup_list:
					print("ok")
					update_channel_data(conn,cur,row['channelid'])
				else :
					print("already updated")
			else:
				db.delete_channel(row['channelid'], cur)
				print("delete")
			print("%d %s %s %s" % (id, row['channeltitle'],row['maincategory'],row['subcategory']))
