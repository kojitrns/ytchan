# coding: utf-8
import pprint
import urllib
import db_handler as db
import random
from twitter import tw_handler as tw

with db.get_connection() as conn:
	with conn.cursor(cursor_factory = db.psycopg2.extras.DictCursor) as cur:
		if not db.check_should_update(conn,cur,2,'video_bot'):
			exit()
		cur.execute('SELECT * FROM video')
		rows = cur.fetchall()
		row = rows[random.randrange(len(rows)-1)]
		tw_new_video = '{}さんの新しい動画。  https://www.youtube.com/watch?v={} https://ytchan.herokuapp.com/{}/video #{}'
		tw_new_video = tw_new_video.format(row['channel_title'],row['video_id'],
			urllib.parse.urlencode({'q':row['main_category']})[2:],row['sub_category'])
		print(tw_new_video)
		tw.tweet(cur, tw_new_video)