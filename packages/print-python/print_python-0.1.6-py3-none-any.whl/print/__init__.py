import os
import logging
import requests

url = os.getenv('PRINT_URL')
token = os.getenv('PRINT_TOKEN')

def print(*args, **kwargs):
	global url, token

	if 'url' in kwargs:
		url = kwargs['url']
		del kwargs['url']

	if 'token' in kwargs:
		token = kwargs['token']
		del kwargs['token']

	if len(args) != 0:
		json = {
			'text': ' '.join([str(arg) for arg in args]),
			'metadata': kwargs,
			'token': token
		}

		try:
			return requests.post(url, json=json, timeout=1)

		except Exception as e:
			logging.error(e)
