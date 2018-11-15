from unittest import TestCase

from Simulator import Simulator


class TestSimulator(TestCase):
    def test_simulate_FCFS(self):
        client_num = 10_000_000
        simulator = Simulator()
        waiting_times = simulator.simulate_FCFS(0.6, client_num)
        self.assertTrue(len(waiting_times) == client_num)
