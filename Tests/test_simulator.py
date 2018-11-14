from unittest import TestCase

from Simulator import Simulator


class TestSimulator(TestCase):
    def test_run_sample_FCFS(self):
        Simulator().run_sample_FCFS(10, 0.6)
