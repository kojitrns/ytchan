# coding: utf-8
import sys,codecs
import pprint
import requests
import dbtest as db

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

def chan_record_gen(chan_data, chan_type):
#chan_data: channel resource
#chandata (channelId, channelTitle, channelType, viewCount, videoCount, subscriberCount, thumbnail_url )
	stat = chan_data['statistics']
	return (chan_data['id'], chan_data['snippet']['title'], chan_type, stat['viewCount'], stat['videoCount'], stat['subscriberCount'],
		chan_data['snippet']['thumbnails']['medium']['url'])

with codecs.open('datalist2','r','utf-8') as f:
    l = f.readlines()
    for category in l:
    	if len(category) > 2 :
    		response = requests.get(
				reqPprefix+'search?',
				params={'key':'AIzaSyD3R2gavNlItHEZWTt-_UOMEwFwMN5reiQ', 'type': 'channel',
				'part': 'snippet', 'q': category.rstrip('\n'), 'regionCode': 'JP', 'maxResults': 5})
    		max_chan = get_highest_chan(response.json()['items'], 'subscriberCount')
    		if max_chan is not None:
    			rec = chan_record_gen(max_chan, category)
    			db.test_add_chan(rec, 'channels')