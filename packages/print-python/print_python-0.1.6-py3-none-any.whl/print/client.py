import requests

class Client(object):

	def __init__(self, host=None, path=None, token=None):
		self.host = host
		self.path = path
		self.token = token

	def text(self, *args, **kwargs):
		return {
			'text': ' '.join([str(arg) for arg in args]),
			'metadata': kwargs
		}

	def post(self, *args, **kwargs):
		json = self.text(*args, **kwargs)
		json.update({'token': self.token})
		return requests.post(f'{self.host}{self.path}', json=json)
