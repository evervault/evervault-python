from .key import Key
from ..errors.evervault_errors import UndefinedDataError, InvalidPublicKeyError
import cryptography

class Client(object):
    def __init__(self):
        self.cage_key = None

    def encrypt_data(self, fetch, data):
        if data is None: raise UndefinedDataError('Data not defined')
        self._fetch_cage_key(fetch)
        if self.cage_key is None or type(self.cage_key) != str: raise InvalidPublicKeyError('Provided public key is invalid')
        if type(data) == dict:
            return self._encrypt_object(data)
        elif self._encryptable_data(data):
            return self._encrypt_string(data)

    def _encrypt_object(self, data):
        pass

    def _encrypt_string(self, data):
        pass

    def _encryptable_data(self, data):
        return data is not None and (
            type(data) == str or 
            type(data) == bool or 
            type(data) == list or 
            type(data) == int or 
            type(data) == float
        )

    def _fetch_cage_key(self, fetch):
        if self.cage_key is None:
            print('Fetching cage key')
            resp = fetch.get('/cages/key')
            self.cage_key = Key(resp['key']).key
