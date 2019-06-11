# coding: utf-8
import pprint
import sys
import urllib
import db_handler as db
import api_handler as ytapi
from twitter import tw_handler as tw
dup_list = []

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
				else :
					print("already updated")
			else:
				db.delete_channel(row['channel_id'], cur)
				print("delete")
			print("%d %s %s %s" % (id, row['channel_title'],row['main_category'],row['sub_category']))

		tweets = []
		tw_text = 'データを更新しました。 カテゴリ->{}  チャンネル数->{} https://ytchan.herokuapp.com/{}/channel #Youtube #{}'
		for category, value in chan_sums.items():
			url_param = urllib.parse.urlencode({'q' : category})
			tweets.append(tw_text.format(category, value ,url_param[2:], category))
			print("%s %d" % (category, value))
		tw.tweet_mul(cur, tweets)