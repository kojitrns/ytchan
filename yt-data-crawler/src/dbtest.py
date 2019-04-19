import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

def get_connection():
	# dsn = os.environ.get('DATABASE_URL')
	return psycopg2.connect(DATABASE_URL, sslmode='require')

with get_connection() as conn:
	with conn.cursor() as cur:
		cur.execute('SELECT * FROM channels;')
		row = cur.fetchall()
		print(row)
		cur.execute("INSERT INTO  channels VALUES (%s, %s, %s, %s, %s)", ('UCd7US-V7-6KvL5uoIE4-Y_A', 'env', 12, 34, 56 ))
	conn.commit()
	