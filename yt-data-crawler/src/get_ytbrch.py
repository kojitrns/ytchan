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
		print(cur_chan['snippet']['title'])

		if max_value < int(cur_chan_stat[target]):
			ret_chan = cur_chan
			max_value = int(cur_chan_stat[target])
	return ret_chan

def chan_record_gen(chan_data, main_name, sub_name):
	stat = chan_data['statistics']
	description = chan_data['snippet']['description']
	keywords = ''
	if 'keywords' in chan_data['brandingSettings']['channel']:
		keywords = chan_data['brandingSettings']['channel']['keywords']
	return (main_name, sub_name, chan_data['id'], chan_data['snippet']['title'], stat['viewCount'], stat['videoCount'], stat['subscriberCount'],
		chan_data['snippet']['thumbnails']['default']['url'], description, keywords)

results_num = 5
higher_num = 5
min_chan_num = 4
main_category = 'Youtuber'
sub_category = main_category
table_name = 'channel'

with open('youtubers') as f:
	l = f.readlines()
	for name in l:
		name = name[:-1]
		if len(name) >= 1:
			response = None
			response = requests.get(
				reqPprefix+'search?',
				params={'key':api_key, 'type': 'channel',
				'part': 'snippet', 'q': name, 'order': 'relevance', 'regionCode': 'JP', 'maxResults': results_num})

			if response is None:
				print("%s %s" % (name,"not found or api error"))
				continue

			chan_data = get_highest_chan(response.json()['items'], 'viewCount')
			print(chan_data['snippet']['title'])
			db.add_channels([chan_record_gen(chan_data, main_category ,sub_category)], table_name)
