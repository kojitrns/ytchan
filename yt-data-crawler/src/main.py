# coding: utf-8
import sys
import pprint
import requests
import db_handler as db
from operator import itemgetter

# sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
reqPprefix = 'https://www.googleapis.com/youtube/v3/'
api_key = 'AIzaSyD3R2gavNlItHEZWTt-_UOMEwFwMN5reiQ'

def get_highest_chan(channels, target):
	ret_chan = None
	max_value = 0

	for chan in channels:
		cur_chan = requests.get(
		    reqPprefix+'channels?', params={'key': api_key,
		    'part': 'statistics,snippet,contentDetails,brandingSettings',
		    'id': chan['snippet']['channelId']}).json()['items'][0]
		cur_chan_stat = cur_chan['statistics']

		if max_value < int(cur_chan_stat[target]):
			ret_chan = cur_chan
			max_value = int(cur_chan_stat[target])
	return ret_chan

def get_sorted_channel_list(channels, target, size):
	ret_chan = None
	max_value = 0
	chan_list = {}

	for chan in channels:
		cur_chan = requests.get(
		    reqPprefix+'channels?', params={'key': api_key,
		    'part': 'statistics,snippet,brandingSettings',
		    'id': chan['snippet']['channelId']}).json()['items'][0]
		chan_list[-int(cur_chan['statistics'][target])] = cur_chan
	chan_list = sorted(chan_list.items())

	if len(chan_list) >= size :
		return chan_list[0:size]
	return None

def get_adding_channel_list(channels):
	max_value = 0
	chan_list = []
	chan_id_list = []

	for chan in channels:
		cur_chan = requests.get(
		    reqPprefix+'channels?', params={'key': api_key,
		    'part': 'statistics,snippet,brandingSettings,contentDetails',
		    'id': chan['snippet']['channelId']}).json()
		if ('items' in cur_chan) and cur_chan['items']:
			chan_data = cur_chan['items'][0]
			if (chan_data['id'] not in chan_id_list and
				evaluate_channel(chan_data)):
				chan_list.append(chan_data)
				chan_id_list.append(chan_data['id'])

	return chan_list

def evaluate_channel(chan_data):
	at_least_value = 1000
	stats = chan_data['statistics']
	if int(stats['videoCount']) < 1:
		return False
	chan_value = int(stats['videoCount']) + int(stats['subscriberCount']) + int(stats['videoCount']);
	return at_least_value < chan_value

def get_latest_video(playlist_id):
	return requests.get(
	    reqPprefix+'playlistItems?', params={'key': api_key,
	    'part': 'snippet', 'playlistId': playlist_id,
	    'maxResults': 1}).json()


results_num = 10
higher_num = 5
min_chan_num = 4
main_category = ''
table_name = 'channel'

with open('category') as f:
	l = f.readlines()
	for category in l:
		category = category[:-1]
		if len(category) >= 1:
			if category.startswith('*'):
				main_category = category[1:]
				print('***'+main_category)
				continue
			print('*'+category)

			response = None
			response = requests.get(
				reqPprefix+'search?',
				params={'key':api_key, 'type': 'channel',
				'part': 'snippet', 'q': category, 'order': 'viewCount', 'regionCode': 'JP', 'maxResults': results_num})

			if response is None:
				print("%s %s" % (category,"None"))
				continue
			chan_list = get_adding_channel_list(response.json()['items'])

			if len(chan_list) < min_chan_num:
				print("shortage category %s %d" % (category, len(chan_list)))
				continue

			recs = []
			for chan in chan_list:
				recs.append(db.chan_record_gen(chan, main_category ,category))
			db.add_channels(recs, table_name)
