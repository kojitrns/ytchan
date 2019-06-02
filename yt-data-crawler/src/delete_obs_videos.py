# coding: utf-8
import pprint
import sys
import time
import db_handler as db

with db.get_connection() as conn:
	with conn.cursor() as cur:
		cur.execute('SELECT * FROM video')
		rows = cur.fetchall()
		for (id, row) in enumerate(rows):
			if not db.is_exist_channel(row[2], cur):
				db.delete_video(row[2], cur)
				print('delete %s' %(row[3]))
