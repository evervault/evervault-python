from unittest import TestCase
from unittest.mock import Mock
import time

from evervault.http.repeated_timer import RepeatedTimer


class TestRepeatedTimer(TestCase):
    def test_timer_is_running_on_init(self):
        mock_object = Mock()
        rt = RepeatedTimer(0.1, mock_object)
        self.assertTrue(rt.running())
        rt.stop()

    def test_timer_function_called_at_interval(self):
        counter = TestRepeatedTimer.Counter()
        rt = RepeatedTimer(0.1, counter.increment)
        self.assertTrue(rt.running())
        time.sleep(0.25)
        rt.stop()
        self.assertEqual(counter.value, 2)

    def test_timer_interval_updated(self):
        counter = TestRepeatedTimer.Counter()
        rt = RepeatedTimer(0.05, counter.increment)
        self.assertTrue(rt.running())
        time.sleep(0.12)
        rt.update_interval(0.1)
        time.sleep(0.25)
        self.assertEqual(counter.value, 4)
        rt.stop()

    def test_timer_will_stop(self):
        mock_object = Mock()
        rt = RepeatedTimer(0.1, mock_object)
        time.sleep(0.12)
        self.assertTrue(rt.running())
        rt.stop()
        self.assertFalse(rt.running())

    class Counter(object):
        def __init__(self):
            self.value = 0
        
        def increment(self):
            self.value += 1
            print("polling")
        