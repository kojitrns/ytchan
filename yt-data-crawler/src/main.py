# coding: utf-8
import sys
import pprint
import requests
import dbtest as db
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

def get_channel_detail_list(channels):
	max_value = 0
	chan_list = []
	chan_idlist = []

	for chan in channels:
		cur_chan = requests.get(
		    reqPprefix+'channels?', params={'key': api_key,
		    'part': 'statistics,snippet,brandingSettings',
		    'id': chan['snippet']['channelId']}).json()
		if ('items' in cur_chan) and cur_chan['items']:
			if (cur_chan['items'][0]['id'] not in chan_idlist):
				chan_list.append(cur_chan['items'][0])
				chan_idlist.append(cur_chan['items'][0]['id'])

	return chan_list

def chan_record_gen(chan_data, main_category, sub_category):
#chan_data: channel resource
#chandata (channelId, channelTitle, channelType, viewCount, videoCount, subscriberCount, thumbnail_url )
	stat = chan_data['statistics']
	return (main_category, sub_category, chan_data['id'], chan_data['snippet']['title'], stat['viewCount'], stat['videoCount'], stat['subscriberCount'],
		chan_data['snippet']['thumbnails']['default']['url'])

with open('category') as f:
	l = f.readlines()
	results_num = 10
	higher_num = 5
	main_category = ''
	min_chan_num = 4
	for category in l:
		category = category[:-1]
		if len(category) > 2 :
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
				# chan_list = get_sorted_channel_list(response.json()['items'], 'subscriberCount', higher_num)
			if response is None:
				continue
			chan_list = get_channel_detail_list(response.json()['items'])

			for chan in chan_list:
				print(chan['snippet']['title'])
			if len(chan_list) < min_chan_num:
				continue
			if chan_list is not None:
				recs = []
				for chan in chan_list:
					recs.append(chan_record_gen(chan, main_category ,category))
				db.test_add_chan(recs, 'channel')

