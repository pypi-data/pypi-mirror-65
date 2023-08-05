from .request import get, post, sess
from .exception import LoginError, URLError, FileError, ConnectionError
from .core import randomAgent
import json, requests, os
from bs4 import BeautifulSoup as bs

class Session:
	def __init__(self):
		self.is_login = False
		self.s = sess()
		self.base = "https://instagram.com"
		self.url = self.base + "/accounts/login/ajax"
		self.csrf = self.s.get(self.base).cookies["csrftoken"]

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
			return j["status"]
			self.s.headers.update({'X-CSRFToken': request.cookies['csrftoken']})
		except:
			return j["status"]

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

	def get_followers(self, name, max=10):
		"Tested"
		data = []
		url = "https://globalinta.com/"
		url += name+"/followers"
		self.s.headers = {"User-Agent":randomAgent()}
		r = self.s.get(url)
		b = bs(r.text, "html.parser")
		for ul in b.findAll("ul", {"class":"users"}):
			a = (str(ul).findAll("a")["href"]).replace("/", "")
			print (str(a))
		return data
