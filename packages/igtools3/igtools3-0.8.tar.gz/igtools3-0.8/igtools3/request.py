import requests

def get(url, data=None, headers=None):
	return requests.get(url, data=data, headers=headers)

def post(url, data=None, headers=None):
	return requests.post(url, data=data, headers=headers)

def sessions():
	return requests.Session()
