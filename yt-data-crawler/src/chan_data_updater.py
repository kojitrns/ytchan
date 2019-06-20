# coding: utf-8
import pprint
import sys
import urllib
import db_handler as db
import api_handler as ytapi
from twitter import tw_handler as tw

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
		row = [db.chan_record_gen(chan_data, old_data['main_category'], old_data['sub_category'])]
		db.add_data_with_conn(row, 'channel', conn, cur)


def is_valid_channel(chan_data):
	return chan_data['view_count'] > 0

# init()

with db.get_connection() as conn:
	with conn.cursor(cursor_factory = db.psycopg2.extras.DictCursor) as cur:
		cur.execute('SELECT * FROM channel')
		rows = cur.fetchall()
		chan_sums = {}
		for (id, row) in enumerate(rows):
			if is_valid_channel(row):
				if not row['main_category'] in chan_sums:
					chan_sums[row['main_category']] = 0

				if not row['channel_id'] in dup_list:
					chan_sums[row['main_category']] += 1
					update_channel_data(conn,cur,row['channel_id'])
				else :
					print("already updated")
			else:
				db.delete_channel(row['channel_id'], cur)
				print("delete")
			print("%d %s %s %s" % (id, row['channel_title'],row['main_category'],row['sub_category']))
		chan_sums_total = 0
		db.check_should_update(conn, cur, 1, 'channel')
		for category, value in chan_sums.items():
			chan_sums_total += value
			print("%s %d" % (category, value))

		tw_text = 'データを更新しました。チャンネル数->{} #Youtube'
		tw.tweet(cur, tw_text.format(chan_sums_total))