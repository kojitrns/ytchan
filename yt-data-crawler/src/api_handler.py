# coding: utf-8
import sys
import pprint
import requests

reqPprefix = 'https://www.googleapis.com/youtube/v3/'
api_key = 'AIzaSyD3R2gavNlItHEZWTt-_UOMEwFwMN5reiQ'


def get_channel_data(channelId):
	return requests.get(
	    reqPprefix+'channels?', params={'key': api_key,
	    'part': 'statistics,snippet,brandingSettings,contentDetails',
	    'id': channelId}).json()['items'][0]
