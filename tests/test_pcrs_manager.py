import unittest
from evervault.http.cagePcrManager import CagePcrManager


class TestCagePcrManager(unittest.TestCase):
    def setUp(self):
        self.app_uuid = "app-123"
        self.cage_1 = "cage_1"
        self.cage_2 = "cage_2"

    def test_get_pcrs(self):
        test_pcrs1 = [{"pcr_8": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"}]
        test_pcrs2 = [{"pcr_8": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"}]

        def test_provider1():
            return test_pcrs1
        
        def test_provider2():
            return test_pcrs2
        
        attestation_data = {
            self.cage_1: test_provider1,
            self.cage_2: test_provider2
        }

        manager = CagePcrManager(attestation_data)
        
        assert manager.get(self.cage_1) == test_pcrs1
        assert manager.get(self.cage_2) == test_pcrs2

    def test_get_hardcoded_pcrs(self):
        test_pcrs_object = {"pcr_8": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"}
        test_pcrs_array = [
            {"pcr_8": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"}, 
            {"pcr_8": "111100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011"}
            ]
        attestation_data = {
            self.cage_1: test_pcrs_object,
            self.cage_2: test_pcrs_array
        }

        manager = CagePcrManager(attestation_data)
        
        assert manager.get(self.cage_1) == [test_pcrs_object]
        assert manager.get(self.cage_2) == test_pcrs_array

    def test_get_pcrs_reload_on_missing(self):
        test_pcrs1 = [{"pcr_8": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"}]

        def test_provider1():
            return test_pcrs1
        
        attestation_data = {
            self.cage_1: test_provider1
        }

        manager = CagePcrManager(attestation_data)

        # Remove pcrs for cage_1 so that we test the reload on a miss
        manager.remove_pcrs_for_cage(self.cage_1)

        assert manager.get(self.cage_1) == test_pcrs1

    # @requests_mock.Mocker()
    # def test_get_attestation_doc_missing_cache_reload(self, mock_request):
    #     self.cage_host = "cage.evervault.com"
    #     self.__mock_attestation_doc(mock_request, self.cage_1)
    #     self.__mock_attestation_doc(mock_request, self.cage_2)
    #     cage_names = [self.cage_1]
    #     doc = AttestationDoc(self.app_uuid, cage_names, "cage.evervault.com")
    #     assert doc.get(self.cage_1) == "123"
    #     assert doc.get(self.cage_2) == "123"

    # @responses.activate
    # def test_get_attestation_doc_cache_poll(self):
    #     responses.add(
    #         responses.GET,
    #         f"https://cage_1.{self.app_uuid}.cage.evervault.com/.well-known/attestation",
    #         json={"attestation_doc": "123"},
    #         status=200,
    #     )
    #     responses.add(
    #         responses.GET,
    #         f"https://cage_1.{self.app_uuid}.cage.evervault.com/.well-known/attestation",
    #         json={"attestation_doc": "newdoc!"},
    #         status=200,
    #     )
    #     self.cage_host = "cage.evervault.com"
    #     cage_names = [self.cage_1]
    #     doc = AttestationDoc(self.app_uuid, cage_names, "cage.evervault.com", 1)
    #     assert doc.get(self.cage_1) == "123"
    #     time.sleep(2)
    #     assert doc.get(self.cage_1) == "newdoc!"
