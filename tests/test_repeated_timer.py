from unittest import TestCase
from unittest.mock import Mock
import time

from evervault.http.repeated_timer import RepeatedTimer


class TestRepeatedTimer(TestCase):
    def test_timer_is_running_on_init(self):
        mock_object = Mock()
        rt = RepeatedTimer(0.1, mock_object)
        self.assertTrue(rt.running())

    def test_timer_function_called_at_interval(self):
        mock_object = Mock()
        rt = RepeatedTimer(0.1, mock_object)
        self.assertTrue(rt.running())
        time.sleep(0.2)
        mock_object.assert_called_once()

    def test_timer_will_stop(self):
        mock_object = Mock()
        rt = RepeatedTimer(0.1, mock_object)
        self.assertTrue(rt.running())
        rt.stop()
        self.assertFalse(rt.running())
