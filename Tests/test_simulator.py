from unittest import TestCase

from Simulator import SimulatorFCFS, SimulatorLCFS


class TestSimulator(TestCase):
    def test_simulate_FCFS(self):
        client_num = 100
        simulator = SimulatorFCFS(0.6)
        for i in range(0, 3200):
            res = simulator.simulate_FCFS(client_num)
            self.assertTrue(len(res[0]) == client_num)
            # print(res[0])
            # print(res[1])
            # print(res[2])

    def test_simulate_LCFS(self):
        client_num = 100
        simulator = SimulatorLCFS(0.6)
        for i in range(0, 3200):
            res = simulator.simulate_LCFS(client_num)
            self.assertTrue(len(res[0]) == client_num)
            # print(res[0])
            # print(res[1])
            # print(res[2])
