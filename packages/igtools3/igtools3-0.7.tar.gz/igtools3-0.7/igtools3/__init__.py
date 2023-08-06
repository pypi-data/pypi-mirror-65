#                Copyright (c) 2020 Billal Fauzan

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

from .request import get, post, sess
from .exception import LoginError, URLError, FileError, ConnectionError, HashtagNotFound, ChangeFailed
from .core import randomAgent, randomPassword
import json, requests, os, re
from bs4 import BeautifulSoup as bs

__author__  = "Billal Fauzan"
__version__ = 0.7
__from__    = "igtools"

def get_postid(user, max=None):
	old = []
	new = []
	if not max:
		max=1
	r = get("https://instagram.com/"+str(user))
	id = re.findall('"id":"..................[0-9]', r.text)
	for a in id:
		if len(old) < max:
			old.append(a.replace('"id":"', ''))
		else:
			break
	return old

class Session:
	def __init__(self):
		self.is_login = False
		self.s = sess()
		self.base = "https://instagram.com"
		self.url = self.base + "/accounts/login/ajax"
		self.csrf = self.s.get(self.base).cookies["csrftoken"]
		counts = ""
		self.data = []
		self.token = []

	def login(self, user, pwd):
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
#		head[Cookie: ig_did=F372CC45-AA29-40AC-9624-51EA4859E4EE; mid=XnPxVQABAAHegRxtl7_yLcvFJVab; csrftoken=giRcFhII7Dw9G5ZGMHbA2hpK3lZJ5iyM; rur=ATN

		self.s.headers = (head)
		r = self.s.get(self.base)
		csrf = r.cookies["csrftoken"]
		self.s.headers.update({'X-CSRFToken': csrf})
		data = {}
		data["username"] = user
		data["password"] = pwd
		request = self.s.post("https://www.instagram.com/accounts/login/ajax/", data=data, allow_redirects=True)
		j = json.loads(request.text)
		try:
			if j["authenticated"] == True:
				self.s.headers.update({'X-CSRFToken': request.cookies['csrftoken']})
				self.s.cookies.update(request.cookies)
				return "ok"
			elif "checkpoint" in request.txt:
				raise CheckpointRequired("Your Account Checkpoint")
		except:
			raise LoginError("Login failed")

	def get_info(self, name):
		" Get Info Account (Tested)"
		data = {}
		try:
			r = get("http://www.insusers.com/"+name+"/followers", headers={"User-Agent":randomAgent()})
			b = bs(r.text, "html.parser")
			for a in b.findAll("li"):
				dat = a.find("a")
				if "followings" in str(dat.get("href")):
					data["followings"] = a.text
				if "followers" in str(dat.get("href")):
					data["followers"] = a.text
			for title in b.findAll("div", {"class":"prright"}):
				data["title"] = str(title).replace("<p>", "").replace("</p>", "").replace("<br/>", "\n").replace('<div class="prright">', '').replace("</div>","")
			return data
		except requests.exception.ConnectionEror:
			raise ConnectionError("No Connection, Please Turn On Your Connection or Check")

	def get_photo_profile(self, name):
		"For Get Link Photo Profile With Link Post (Tested)"
		try:
			data = {}
			url = self.base+"/"+name
			r = self.s.get(url, headers={"User-Agent":randomAgent()})
			b = bs(r.text, "html.parser")
			try:
				photo = b.find("meta", {"property":"og:image"})["content"]
				data["photo"] = photo
			except TypeError:
				data["error"] = "Failed To Get Link Profile"
			return data
		except Exception as E:
			raise ConnectionError(str(E))

	def download(self, link, file):
		"Tested"
		if os.path.isfile(file):
			try:
				data = self.s.get(link)
				save = open(file, "wb")
				save.write(data.content)
			except Exception as E:
				raise URLE3rror(str(E))
		else:
			raise FileError("File '%s' already exists"%(file))

	def csrftoken(self):
		r = self.s.get("https://instagram.com")
		token = self.s.cookies["csrftoken"]
		self.s.headers.update({'X-CSRFToken': token})

	def followerCount(self, account_id, max=10, end_cursor=""):
		"""Tools Ini Masih Tahap Pengembangan
		Thanks to: https://github.com/realsirjoe/instagram-scraper/blob/master/igramscraper/instagram.py"""
		counts = []
		var = {}
		var["id"] = account_id
		var["first"] = str(max)
		var["after"] = end_cursor
		url = "https://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%s" % (json.dumps(var))
		self.csrftoken()
		r = self.s.get(url).json()
		try:
			counts.append(r["data"]["user"]["edge_followed_by"]["count"])
		except: pass
		return counts

	def get_followers_name(self, account_id, max=10, end_cursor=""):
		name = []
		while True:
			var = {}
			var["id"] = account_id
			var["first"] = str(max)
			var["after"] = end_cursor
			url = "https://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%s" % (json.dumps(var))
			self.csrftoken()
			r = self.s.get(url).json()
			pageInfo = r["data"]["user"]["edge_followed_by"]["page_info"]
			if pageInfo["has_next_page"]:
				end_cursor = pageInfo["end_cursor"]
			for a in r["data"]["user"]["edge_followed_by"]["edges"]:
				nama = a["node"]["username"]
				name.append(nama)
			if not pageInfo["has_next_page"]:
				break
		return name

	def search_by_hashtag(self, tag):
		url = "https://www.instagram.com/explore/tags/"+str(tag)+"/?__a=1"
		r = get(url)
		try:
			j = json.loads(r.text)
			self.counts = str(j["graphql"]["hashtag"]["edge_hashtag_to_media"]["count"]) #interger
#			self.data.append(self.count)
			return ""
		except:
			raise HashtagNotFound("Hash Tag '%s' not found" % (str(tag)))

	def search_by_name(self, name):
		data = []
		url = "https://www.instagram.com/web/search/topsearch/?context=blended&query="
		url += str(name)
		r = requests.get(url)
		j = json.loads(r.text)
		for a in j["users"]:
			data.append(a["user"]["username"])
		return data

	def changePassword(self, user, old=None, new=None):
		""" Thanks To: https://github.com/Xractz/mbi
		Tools is no tested

		If password new NULL (None) then random new password"""
		if not new:
			new = randomPassword()
		else: pass
		self.login(user, old)
		# data to post
		data = {}
		data["old_password"]  = old
		data["new_password1"] = new
		data["new_password2"] = new
		r = self.s.post("https://www.instagram.com/accounts/password/change/", data=data).text
		check = re.findall(r"\"status\"\: \"(.*?)\"", r)[0]
		if "ok" in check.lower():
			d = []
			d.append("ok")
			d.append(new)
			return d
		else:
			raise ChangeFailed
