import requests
from bs4 import BeautifulSoup

class KeywordGenerator():
	def __init__(self):
		self.keyword_list = set()

		NY_TIMES = "https://www.nytimes.com/"
		r = requests.get(NY_TIMES)
		soup = BeautifulSoup(r.text, features="html.parser")
		for a_tag in soup.find_all("a"):
			if(a_tag['href'].split(".")[-1] == "html"):
				req_article = requests.get("{}{}".format(NY_TIMES, a_tag['href']))
				soup = BeautifulSoup(req_article.text, features = "html.parser")
				try:
					article_body_paragraph = soup.find("section", {"name": "articleBody"}).find_all("p")
					for paragraph in article_body_paragraph:
						self.makeKeyword(paragraph.text)
				except:
					continue


	def makeKeyword(self, text):
		keywords = text.split(" ")
		for keyword in keywords:
			if(keyword.isalnum()):
				self.keyword_list.add(keyword)

	def getKeywordList(self):
		return self.keyword_list
