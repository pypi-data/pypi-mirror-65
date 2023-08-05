import requests

class test_client():
	def get(self,path):
		r = requests.get('http://app:5000' + path)
		self.data = str.encode(r.text)
		self.status_code = r.status_code
		return self

