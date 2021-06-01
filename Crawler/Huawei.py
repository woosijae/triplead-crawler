import requests
from bs4 import BeautifulSoup
import math
from Utils import SAVEDIR
from Uploader import Uploader
import os.path
import sqlite3

class Huawei():
	def __init__(self):
		print("[Log] Huawei::init()");
		self.Uploader = Uploader()
		self.db = sqlite3.connect("{}/{}".format(SAVEDIR, "meta.db"))
		with self.db as con:
			cursor = con.cursor()
			cursor.execute('''CREATE TABLE if not exists apk_meta
					(app_name TEXT, download_count TEXT, release_date TEXT, store TEXT)''')
			cursor.execute('''CREATE TABLE if not exists error_log
					(description TEXT)''')

	def crawlAndUpload(self, keyword):
		print("[Log] Huawei::crawlAndUpload ({})".format(keyword))
		URL = "https://appstore.huawei.com/search/"
		headers = {
			"Host": "appstore.huawei.com", 
			"Connection": "keep-alive", 
			"Upgrade-Insecure-Requests": "1", 
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36", 
			"Sec-Fetch-Mode": "navigate", 
			"Sec-Fetch-User": "?1", 
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3", 
			"Sec-Fetch-Site": "same-origin", 
			"Referer": "https://appstore.huawei.com/", 
			"Accept-Encoding": "gzip, deflate, br", 
			"Accept-Language": "en-us,ko;q=0.9,en-US;q=0.8,en;q=0.7", 
			"Cookie": "cs6k_langid=en_us; hwsso_login="""
		}

		r = self.requestGetIgnoreError("{}{}".format(URL, keyword), headers)
		soup = BeautifulSoup(r.text, features="html.parser")
		total_app_count = soup.find("span", {"class": "sres"}).text.split(":")[1]

		view_on_page = 24
		for page in range(1, math.ceil(int(total_app_count) / view_on_page) + 1):
			print ("[#] {} Crawling... {} / {} ({} %)".format(keyword, page, (math.ceil(int(total_app_count) / view_on_page)), int((page / (math.ceil(int(total_app_count) / view_on_page))) * 100)))
			r = self.requestGetIgnoreError(("{}{}/{}".format(URL, keyword, page)), headers)
			soup = BeautifulSoup(r.text, features="html.parser")

			apk_datas = soup.findAll("div", {"class": "game-info whole"})
			for apk_data in apk_datas:

				search = apk_data.find("p", {"class": "date"})
				if search == None:
					release_date = 'Error'
					print("[!] {} - {} has no release_date".format(keyword, page))
					self.insertError("{} - {} has no release_date".format(keyword, page))
					continue
				else:
					release_date = search.text.replace("ReleseDate:", "")

				down_obj = apk_data.find("div", {"class": "app-btn"})
				try:
					download_obj_span = down_obj.findAll("span")[1]
					if(download_obj_span.text.find("Download") > -1):
						download_count_liter = download_obj_span.text.split(":")[1].strip()
						if(ord(download_count_liter[-1]) == 135):
							download_count = str(int(download_count_liter[:-3])/float(100)) + " Million"
						elif(ord(download_count_liter[-1]) == 191):
							download_count = str(int(download_count_liter[:-3])/float(10)) + " Billion"
						else:
							download_count = download_count_liter
					else:
						# Pass pay APK
						print("[!] {} - {} has premium APK".format(keyword, page))
						self.insertError("{} - {} has premium APK".format(keyword, page))
						continue
				except:
					download_count = "Unknown"
					print("[!] {} - {} has no download_count data".format(keyword, page))
					self.insertError("{} - {} has no download_count data".format(keyword, page))

				download_button = apk_data.find("a", {"class": "btn-blue down"})
				if (len(download_button['onclick'].split(",")) < 5):
					# Do not download pay APK
					continue
				download_link = download_button['onclick'].split("','")[5]
				processed_link = download_link.split("?")[0]
				file_name = processed_link.split('/')[-1]
				save_name = "{}/{}/{}".format(SAVEDIR, "HuaweiApps", file_name)
				if not (os.path.isfile(save_name)):
					self.downloadAppIgnoreError(processed_link, save_name, keyword, page)
					uploaded_app_id = self.Uploader.uploadApk(save_name)
					if(uploaded_app_id != False):
						if(self.Uploader.setTag(uploaded_app_id, "Huawei")):
							self.insertMeta(file_name, download_count, release_date)
							print("[+] Upload Success : {}".format(file_name))
						else:
							print("[-] Set Tag Failed : {} - {}".format(file_name, uploaded_app_id))
					else:
						print("[-] Upload Failed : {}".format(file_name))
				else:
					print("[-] {} Already exist.".format(file_name))

	def downloadApp(self, apk_link, save_name):
		print("[Log] Huawei::downloadApp ({}, {})".format(apk_link, save_name))
		r = requests.get(apk_link, allow_redirects=True)
		open(save_name, 'wb').write(r.content)

	def downloadAppIgnoreError(self, apk_link, save_name, keyword, page):
		print("[Log] Huawei::downloadAppIgnoreError ({}, {}, {}, {})".format(apk_link, save_name, keyword, page))
		while True:
			try:
				if(save_name.isprintable()):
					self.downloadApp(apk_link, save_name)
				else:
					self.insertError("{} is not printable. ({})".format(save_name, apk_link))
				return
			except KeyboardInterrupt:
				print("[!] Stop Huawei crawler")
				exit()
			except:
				self.insertError("{} - {} Download Error ({} - {} Page)".format(save_name, apk_link, keyword, page))
				print("[!] Download Error! Retry... {} - {} - {} - {}".format(save_name, apk_link, keyword, page))	


	def requestGetIgnoreError(self, url, headers):
		print("[Log] Huawei::requestGetIgnoreError({}, {})".format(url, headers))
		while True:
			try:
				return requests.get(url, headers=headers)
			except KeyboardInterrupt:
				print("[!] Stop Huawei crawler while request page")
				exit()
			except:
				print("[!] Page request Error! Retry... {}".format(url))	

	def insertMeta(self, apk_name, down_count, release_date):
		print("[Log] Huawei::insertMeta({}, {}, {})".format(apk_name, down_count, release_date))
		with self.db as con:
			cursor = con.cursor()
			cursor.execute('''INSERT INTO apk_meta VALUES
				(?, ?, ?, ?)''', (apk_name, down_count, release_date, "Huawei"))

		self.db.commit()

	def insertError(self, description):
		print("[Log] Huawei::insertError({})".format(description))
		with self.db as con:
			cursor = con.cursor()
			cursor.execute('''INSERT INTO error_log VALUES
				(?)''', (description, ))
		self.db.commit()