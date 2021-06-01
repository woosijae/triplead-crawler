import requests
from json import loads
from Utils import TRIPLE_AD_URL
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class Uploader():
	def __init__(self):
		pass

	def uploadApk(self, fpath):
		print("[Log] uploadApk({})".format(fpath))
		# file upload
		try:
			url = '{}/apk/upload'.format(TRIPLE_AD_URL)
			files = {
			  'file': (fpath.split('/')[-1], open(fpath,'rb'), 'application/vnd.android.package-archive')
			}
			res = requests.post(url, files=files, verify=False)
			if res.status_code != 200:
			 	return False

			data = loads(res.text)
			if data['status'] != 'ok':
			 	return False

			app_id = data['message']['id']
			return app_id
		except KeyboardInterrupt:
			exit()
		except requests.exceptions.ConnectionError:
			return False
		except:
			print("[!] Upload Error! Retry ... {}".format(fpath))
			self.uploadApk(fpath)


	def setTag(self, app_id, tag_name):
		print("[Log] setTag({}, {})".format(app_id, tag_name))
		try:
			# set tag
			url = '{}/apk/{}/update'.format(TRIPLE_AD_URL, app_id)
			data = {
				'type': 'tags',
				'value': tag_name # "Huawei"
			}
			res = requests.post(url, data=data, verify=False)
			if res.status_code != 200:
				return False

			data = loads(res.text)
			if data['status'] != 'ok':
				return False

			return True
		except KeyboardInterrupt:
			exit()
		except:
			print("[!] SetTag Error! Retry ... {}, {}".format(app_id, tag_name))
			self.setTag(app_id, tag_name)