from .http.request import Request

class Client(object):

	def __init__(
		self, 
		api_key = 'your_teams_api_key', 
		request_timeout = 30,
		base_url = 'https://api.evervault.com', 
		base_run_url = 'https://cage.run'
	):
		self.api_key = api_key
		self.base_url = base_url
		self.base_run_url = base_run_url
		self.request = Request(api_key, request_timeout)

	@property
	def _auth(self):
		return (self.api_key, '')

	def encrypt(self):
		pass

	def run(self, cage_name, params):
		pass

	def encrypt_and_run(self, cage_name, params):
		pass

	def get(self, path, params = {}):
		return self.request.make_request('GET', self.url(path), params)

	def post(self, path, params):
		return self.request.make_request('POST', self.url(path), params)

	def put(self, path, params):
		return self.request.make_request('PUT', self.url(path), params)

	def delete(self, path, params):
		return self.request.make_request('DELETE', self.url(path), params)

	def url(self, path):
		return self.base_url + path
