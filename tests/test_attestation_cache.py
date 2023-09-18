import unittest
from evervault.http.attestationdoc import AttestationDoc
from unittest.mock import patch
import pytest
import requests_mock
import time
from evervault.errors.evervault_errors import AttestationDocCacheError
import responses


class TestAttestationDocCache(unittest.TestCase):
    def setUp(self):
        self.app_uuid = "app-123"
        self.cage_1 = "cage_1"
        self.cage_2 = "cage_2"

    @requests_mock.Mocker()
    def test_get_attestation_doc(self, mock_request):
        self.cage_host = "cage.evervault.com"
        self.__mock_attestation_doc(mock_request, self.cage_1)
        self.__mock_attestation_doc(mock_request, self.cage_2)
        cage_names = [self.cage_1, self.cage_2]
        doc = AttestationDoc(self.app_uuid, cage_names, "cage.evervault.com")
        assert doc.get(self.cage_1) == "123"
        assert doc.get(self.cage_2) == "123"

    @requests_mock.Mocker()
    def test_get_attestation_doc_missing_cache_reload(self, mock_request):
        self.cage_host = "cage.evervault.com"
        self.__mock_attestation_doc(mock_request, self.cage_1)
        self.__mock_attestation_doc(mock_request, self.cage_2)
        cage_names = [self.cage_1]
        doc = AttestationDoc(self.app_uuid, cage_names, "cage.evervault.com")
        assert doc.get(self.cage_1) == "123"
        assert doc.get(self.cage_2) == "123"

    @responses.activate
    def test_get_attestation_doc_cache_poll(self):
        responses.add(
            responses.GET,
            f"https://cage_1.{self.app_uuid}.cage.evervault.com/.well-known/attestation",
            json={"attestation_doc": "123"},
            status=200,
        )
        responses.add(
            responses.GET,
            f"https://cage_1.{self.app_uuid}.cage.evervault.com/.well-known/attestation",
            json={"attestation_doc": "newdoc!"},
            status=200,
        )
        self.cage_host = "cage.evervault.com"
        cage_names = [self.cage_1]
        doc = AttestationDoc(self.app_uuid, cage_names, "cage.evervault.com", 1)
        assert doc.get(self.cage_1) == "123"
        time.sleep(2)
        assert doc.get(self.cage_1) == "newdoc!"

    def __mock_attestation_doc(self, mock_request, cage_name):
        url = f"https://{cage_name}.{self.app_uuid}.cage.evervault.com/.well-known/attestation"
        mock_request.get(
            url,
            json={
                "attestation_doc": "123",
            },
        )
