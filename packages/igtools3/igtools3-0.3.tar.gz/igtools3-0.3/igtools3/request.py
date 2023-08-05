import requests
from .exception import ConnectionError

def get(url, headers=None, redirect=False):
	r = requests.get(url, headers=headers, allow_redirects=redirect)
	return r

def post(url, headers=None, data=None):
	r = requests.post(url, data=data, headers=headers)
	return r

def sess():
	try:
		sesion = requests.Session()
		return sesion
	except requests.exceptions.ConnectionError:
		raise ConnectionError("No Connection, Please Turn On Your Connection or Check")
