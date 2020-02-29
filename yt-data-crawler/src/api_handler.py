# coding: utf-8
import sys
import time
import pprint
import requests

reqPprefix = 'https://www.googleapis.com/youtube/v3/'
api_key = 'AIzaSyAisjvEMDBsSosPXXVuOV1U1PcGqlomEvg'

def get_channel_data(channel_id, retry_limit):
	chan_data = requests.get(
	    reqPprefix+'channels?', params={'key': api_key,
	    'part': 'statistics,snippet,brandingSettings,contentDetails',
	    'id': channel_id})
	chan_data = error_check(chan_data)
	if  chan_data is None:
		if retry_limit == 0:
			return None
		print("retry! \n\n\n\n")
		time.sleep(3)
		return get_channel_data(channel_id, retry_limit - 1)

	return chan_data

def get_latest_video_data(uplist_id, retry_limit):
	videos = None
	videos = requests.get(
	    reqPprefix+'playlistItems?', params={'key': api_key,
	    'part': 'snippet',
	    'playlistId': uplist_id})
	videos = error_check(videos)
	if  videos is None:
		if retry_limit == 0:
			return None
		print("retry! \n\n\n\n")
		time.sleep(3)
		return get_latest_video_data(uplist_id, retry_limit - 1)

	video_id = videos['snippet']['resourceId']['videoId']
	video_data = requests.get(
	    reqPprefix+'videos?', params={'key': api_key,
	    'part': 'snippet,contentDetails,statistics',
	    'id': video_id})
	video_data = error_check(video_data)

	if video_data is None:
		if retry_limit == 0:
			return None
		print("retry! \n\n\n\n")
		time.sleep(3)
		return get_latest_video_data(uplist_id, retry_limit - 1)

	return video_data

def error_check(ret):
	if ret is None :
		pprint.pprint(ret)
		return None
	ret = ret.json()
	if 'items' in ret and len(ret['items']) > 0:
		return ret['items'][0]
	pprint.pprint(ret)
	return None

def get_category(category_id):
	return requests.get(
	    reqPprefix+'videoCategories?', params={'key': api_key,
	    'part': 'snippet',
	    'id': category_id}).json()
