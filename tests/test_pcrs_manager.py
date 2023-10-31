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
