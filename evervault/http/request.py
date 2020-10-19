
from datetime import datetime
from .errors import error_handler

import json
import os
import requests
import certifi

class Request(object):

	def __init__(self, api_key):
		self.http_session = requests.Session()
		self.timeout = 30
		self.api_key = api_key

	def make_request(self, method, url, params=None):
		""" Construct an API request, send it to the API, and parse the
		response. """
		from evervault import __version__

		req_params = self._build_headers(method, params, __version__)

		if self.http_session is None:
			resp = requests.request(method, url, timeout=self.timeout,verify=certifi.where(), **req_params)
		else:
			resp = self.http_session.request(method, url, timeout=self.timeout, verify=certifi.where(), **req_params)

		parsed_body = self.parse_body(resp)
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

	def parse_body(self, resp):
		if resp.content and resp.content.strip():
			try:
				decoded_body = resp.content.decode(
					resp.encoding or resp.apparent_encoding)
				return json.loads(decoded_body)
			except ValueError:
				error_handler.raise_errors_on_failure(resp)
				