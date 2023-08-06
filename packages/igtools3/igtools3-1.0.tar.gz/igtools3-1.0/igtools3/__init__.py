from .exceptions import LoginError, FailedScrap, LoginRequired, ChangeFailed, ListError
from .request import get, post, sessions
from .config import inUrl, url, randomAgent, readFile, randomPassword, defaultHeader
import json, re

class Information:
	def __init__(self, user):
		self.data = None
		self.ses = sessions()
		self.user = user

	@property
	def id(self):
		try:
			data = self.data["graphql"]["user"]
			return data["id"]
		except KeyError:
			return None

	def get_info(self):
		url = "https://www.instagram.com/"+str(self.user)+"/?__a=1"
		ref = "https://www.instagram.com/"+str(self.user)
		defaultHeader()["Referer"] = ref
#		print (defaultHeader())
		self.ses.headers = defaultHeader()
		r = self.ses.get(url).json()
		self.data = r

class Account:
	def __init__(self, user, pw):
		self.user = user
		self.pw = pw
		self.s = sessions()
		self.data = {}

	@property
	def isLogin(self):
		try:
			return self.data["logged"]
		except KeyError:
			self.data["logged"] = False
			return self.data["logged"]
	@property
	def message(self):
		try:
			return self.data["message"]
		except KeyError:
			self.data["message"] = "no message"
			return self.data["message"]

	@property
	def status(self):
		try:
			return self.data["status"]
		except KeyError:
			self.data["status"] = False
			return self.data["status"]

	def csrftoken(self):
		r = self.s.get(url)
		csrft = r.cookies["csrftoken"]
		self.s.headers.update({'X-CSRFToken': csrft})

	def login(self):
		# Set Headers
		head = {}
		head["Host"]            = "www.instagram.com"
		head["Origin"]          = "https://www.instagram.com"
		head["X-IG-WWW-Claim"]  = "0"
		head["CSP"]             = "active"
		head["Content-Type"]    = "application/x-www-form-urlencoded"
		head["X-Requested-With"]= "XMLHttpRequest"
		head["User-Agent"]      = randomAgent()
		head["Referer"]         = "https://www.instagram.com/accounts/login/"
		head["Accept-Encoding"] = "gzip, deflate"
		head["Accept-Language"] = "id-ID,en-US;q=0.8"
		self.s.headers = head

		# Set Data to post
		data = {}
		data["username"] = self.user
		data["password"] = self.pw

		# Get and set csrftoken
		self.csrftoken()

		# Post to url
		req = self.s.post("https://www.instagram.com/accounts/login/ajax/", data=data, allow_redirects=True)
		r = req.json()

		# Check
		if r["authenticated"] == True:
			self.s.headers.update({'X-CSRFToken': req.cookies["csrftoken"]})
			self.s.cookies.update(req.cookies)
			self.data["status"] = True
			self.data["logged"] = True
			self.data["message"] = "Success login"
		else:
			self.data["status"] = False
			self.data["logged"] = False
			self.data["message"] = "Failed login"

	def changePassword(self, new=None):
		# If new (null)
		if not new:
			new = randomPassword()
		else:
			pass
		if self.data["logged"]: pass
		else:
#			del self.data[:]
			self.data["status"] = False
			self.data["message"] = "Please login"
			return self.data

		# dsta to post
		data = {}
		data["old_password"] = self.pw
		data["new_password1"] = new
		data["new_password2"] = new

		# post to url
		r = self.s.post("https://www.instagram.com/accounts/password/change/", data=data).text

		# check
		if "ok" in (re.findall(r"\"status\"\: \"(.*?)\"", r)[0]).lower():
			self.data["status"] = True
			self.data["message"] = "Success to change password"
		else:
			self.data["status"] = False
			self.data["message"] = "Failed to change password"

	def follow(self, usr):
		"Thanks to: igtools"
#		if not usr:
#			usr = "igtools3.dev"

		if self.data["logged"]: pass
		else:
			self.data["status"] = False
			self.data["message"] = "Please login"
			return self.data

		if str(usr).isdigit():
			pass
		else:
			info = Information(usr)
			info.get_info()
			usr = info.id
		if self.data["message"]:
			del self.data["message"]
		cek = self.s.post("https://www.instagram.com/web/friendships/%s/follow/" % (usr), allow_redirects=True).json()
		if cek["result"] == "following" and cek["status"] == "ok":
			self.data["status"] = True
			self.data["message"] = "Success To Follow"
			self.data["user"] = usr
		else:
			self.data["status"] = False
			self.data["message"] = "Failed To Follow"
		return self.data
