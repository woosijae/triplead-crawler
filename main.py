from Crawler import Huawei, Baidu, TFpp
from Utils import KeywordGenerator, SAVEDIR, SUPPORTED_CRAWLER
from json import loads
import requests
import sys
import os

def printUsageAndExit():
	print ("[#] Usage: python {} [Huawei|Baidu|TFpp]".format(os.path.realpath(__file__)))
	print ("[#] Example: python {} Huawei".format(os.path.realpath(__file__)))
	exit()

if(len(sys.argv) < 2):
	printUsageAndExit()
if(sys.argv[1] not in SUPPORTED_CRAWLER):
	print("[!] Error! SUPPORTED_CRAWLER: {}".format(SUPPORTED_CRAWLER))
	printUsageAndExit()

print("[#] Generate Keywords from NY Times.")
keyword_gen = KeywordGenerator()
keyword_set = keyword_gen.getKeywordList()
keyword_count = 0

if(sys.argv[1] == "Huawei"):
	HuaweiCrawler = Huawei()
	for keyword in keyword_set:
		keyword_count = keyword_count + 1
		print("[#] {} start Huawei Crawler {} / {} ({} %)".format(keyword, keyword_count, len(keyword_set), int(keyword_count/len(keyword_set) * 100)))
		HuaweiCrawler.crawlAndUpload(keyword)

elif(sys.argv[1] == "Baidu"):
	BaiduCrawler = Baidu()
	for keyword in keyword_set:
		keyword_count = keyword_count + 1
		print("[#] {} start Baidu Crawler {} / {} ({} %)".format(keyword, keyword_count, len(keyword_set), int(keyword_count/len(keyword_set) * 100)))
		BaiduCrawler.crawlAndUpload(keyword)

elif(sys.argv[1] == "TFpp"):
	TFppCrawler = TFpp()
	for keyword in keyword_set:
		keyword_count = keyword_count + 1
		print("[#] {} start TFpp Crawler {} / {} ({} %)".format(keyword, keyword_count, len(keyword_set), int(keyword_count/len(keyword_set) * 100)))
		TFppCrawler.crawlAndUpload(keyword)

else:
	printUsageAndExit()
