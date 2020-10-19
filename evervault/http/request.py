
from datetime import datetime
from .errors import error_handler

import json
import os
import requests
import certifi

class Request(object):

	def __init__(self, api_key, timeout = 30):
		self.http_session = requests.Session()
		self.timeout = timeout
		self.api_key = api_key

	def make_request(self, method, url, params=None):
		from evervault import __version__

		req_params = self._build_headers(method, params, __version__)

		request_object = requests if self.http_session is None else self.http_session
		resp = self._execute_request(request_object, method, url, req_params)

		parsed_body = self._parse_body(resp)
		error_handler.raise_errors_on_failure(resp, parsed_body)
		return parsed_body

	def _build_headers(self, method, params, version):
		req_params = {}
		headers = {
				'User-Agent': 'evervault-python/' + version,
				'AcceptEncoding': 'gzip, deflate',
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'Api-Key': self.api_key
		}
		if method in ('POST', 'PUT', 'DELETE'):
			req_params['data'] = json.dumps(params, cls=json.JSONEncoder)
		elif method == 'GET':
			req_params['params'] = params

		req_params['headers'] = headers
		return req_params

	def _execute_request(self, request_object, method, url, req_params):
		return request_object.request(
			method, 
			url, 
			timeout=self.timeout, 
			verify=certifi.where(), 
			allow_redirects = False, 
			**req_params
			)

	def _parse_body(self, resp):
		if resp.content and resp.content.strip():
			try:
				decoded_body = resp.content.decode(
					resp.encoding or resp.apparent_encoding)
				return json.loads(decoded_body)
			except ValueError:
				error_handler.raise_errors_on_failure(resp)
				