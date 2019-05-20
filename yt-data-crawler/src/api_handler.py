# coding: utf-8
import sys
import pprint
import requests

reqPprefix = 'https://www.googleapis.com/youtube/v3/'
api_key = 'AIzaSyD3R2gavNlItHEZWTt-_UOMEwFwMN5reiQ'


def get_channel_data(channel_id):
	return requests.get(
	    reqPprefix+'channels?', params={'key': api_key,
	    'part': 'statistics,snippet,brandingSettings,contentDetails',
	    'id': channel_id}).json()['items'][0]

def get_latest_video_data(uplist_id):
	video_id = None
	video_id = requests.get(
	    reqPprefix+'playlistItems?', params={'key': api_key,
	    'part': 'snippet',
	    'playlistId': uplist_id})
	if video_id is None:
		print("can't get playlistItem")
		return

	video_id = video_id.json()
	if not 'items' in video_id:
		print(uplist_id)
		pprint.pprint(video_id)
		return None
	video_id = video_id['items'][0]['snippet']['resourceId']['videoId']

	return requests.get(
	    reqPprefix+'videos?', params={'key': api_key,
	    'part': 'snippet,contentDetails,statistics',
	    'id': video_id}).json()['items'][0]

def get_category(category_id):
	return requests.get(
	    reqPprefix+'videoCategories?', params={'key': api_key,
	    'part': 'snippet',
	    'id': category_id}).json()
