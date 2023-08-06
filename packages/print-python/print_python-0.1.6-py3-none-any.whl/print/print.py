import requests

class Print(object):

	def __init__(self, url, token):
		self.url = url
		self.token = token
		self.json = {'token': self.token}

		# Enable keep-alive and connection-pooling.
		self.session = requests.session()

	def post(self, text):
		self.json.update({'text': text})
		return self.session.post(self.url, json=self.json)
