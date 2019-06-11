# coding: utf-8
import os, sys
import json
import pprint
import time
from requests_oauthlib import OAuth1Session
sys.path.append('..')
import db_handler as db

DATABASE_URL = os.environ['DATABASE_URL']

def get_tw_session(cur):
	if cur is not None:
		cur.execute('SELECT * FROM twitter')
		keys = cur.fetchone()
		twitter = OAuth1Session(keys[0], keys[1], keys[2], keys[3])
		return twitter

	with db.get_connection() as conn:
		with conn.cursor() as cur:
			cur.execute('SELECT * FROM twitter')
			keys = cur.fetchone()
	twitter = OAuth1Session(keys[0], keys[1], keys[2], keys[3])
	return twitter

def tweet(cur, text):
	twitter = get_tw_session(cur)
	params = {"status" : text}
	url = "https://api.twitter.com/1.1/statuses/update.json"	
	res = twitter.post(url, params = params)

	if res.status_code == 200:
	    print("%s %s" % (text, "Success."))
	else:
	    print("Failed. : %d"% res.status_code)

def tweet_mul(cur, texts):
	twitter = get_tw_session(cur)
	url = "https://api.twitter.com/1.1/statuses/update.json"	

	for text in texts:
		params = {"status" : text}
		res = twitter.post(url, params = params)		
		if res.status_code == 200:
		    print("%s %s" % (text, "Success."))
		else:
		    print("Failed. : %d"% res.status_code)
		time.sleep(3)

def get_tweets(cur, usr_id, number):
	twitter = get_tw_session()
	url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
	params ={'count' : number, 'user_id' : usr_id}
	res = twitter.get(url, params = params)

	if res.status_code == 200:
	    timelines = json.loads(res.text)
	    for line in timelines:
	        print(line['user']['name']+'::'+line['text'])
	        print(line['created_at'])
	        print('*******************************************')
	else:
	    print("Failed: %d" % res.status_code)