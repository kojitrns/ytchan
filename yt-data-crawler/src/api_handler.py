# coding: utf-8
import sys
import time
import pprint
import requests

reqPprefix = 'https://www.googleapis.com/youtube/v3/'
api_key = 'AIzaSyD3R2gavNlItHEZWTt-_UOMEwFwMN5reiQ'


def get_channel_data(channel_id):
	chan_data = requests.get(
	    reqPprefix+'channels?', params={'key': api_key,
	    'part': 'statistics,snippet,brandingSettings,contentDetails',
	    'id': channel_id})
	chan_data = error_check(chan_data)
	if  chan_data is None:
		print("retry! \n\n\n\n")
		time.sleep(3)
		return get_channel_data(channel_id)

	return chan_data

def get_latest_video_data(uplist_id):
	videos = None
	videos = requests.get(
	    reqPprefix+'playlistItems?', params={'key': api_key,
	    'part': 'snippet',
	    'playlistId': uplist_id})
	videos = error_check(videos)
	if  videos is None:
		print("retry! \n\n\n\n")
		time.sleep(3)
		return get_latest_video_data(uplist_id)

	video_id = videos['snippet']['resourceId']['videoId']
	video_data = requests.get(
	    reqPprefix+'videos?', params={'key': api_key,
	    'part': 'snippet,contentDetails,statistics',
	    'id': video_id})
	video_data = error_check(video_data)

	if video_data is None:
		print("retry! \n\n\n\n")
		time.sleep(3)
		return get_latest_video_data(uplist_id)

	return video_data

def error_check(ret):
	if ret is None :
		return None
	ret = ret.json()
	if 'items' in ret:
		return ret['items'][0]
	return None

def get_category(category_id):
	return requests.get(
	    reqPprefix+'videoCategories?', params={'key': api_key,
	    'part': 'snippet',
	    'id': category_id}).json()
