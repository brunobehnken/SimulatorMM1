from unittest import TestCase

from Simulator import SimulatorFCFS, SimulatorLCFS
from Statistics import Statistics


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

    def test_transient_phase_FCFS(self):
        simulator = SimulatorFCFS(0.2)
        simulator.transient_phase()

    def test_transient_phase_LCFS(self):
        simulator = SimulatorLCFS(0.2)
        simulator.transient_phase()

    def test_FCFS(self):
        """Prototype for Master.py"""
        stat = Statistics()
        simulator = SimulatorLCFS(0.4)
        simulator.transient_phase()
        res = simulator.simulate_LCFS(1_000_000)
        mean_w = stat.calculate_mean(res[0])
        var_w = stat.calculate_variance(res[0], mean_w)
        mean_nq = stat.calculate_mean(res[1])
        mean_nq2 = sum(res[1])/res[2]
        var_nq = stat.calculate_variance(res[1], mean_nq)
        var_nq2 = stat.calculate_variance(res[1], mean_nq2)
        center_ew, lower_ew, upper_ew, precision_ew = stat.confidence_interval_for_mean(mean_w, var_w, len(res[0]), 0.95)
        center_vw, lower_vw, upper_vw, precision_vw = stat.confidence_interval_for_variance(var_w, len(res[0]), 0.95)
        center_enq, lower_enq, upper_enq, precision_enq = stat.confidence_interval_for_mean(mean_nq, var_nq,
                                                                                            len(res[1]), 0.95)
        center_enq2, lower_enq2, upper_enq2, precision_enq2 = stat.confidence_interval_for_mean(mean_nq2, var_nq2,
                                                                                                res[2], 0.95)
        center_vnq, lower_vnq, upper_vnq, precision_vnq = stat.confidence_interval_for_variance(var_nq,
                                                                                                len(res[1]), 0.95)
        center_vnq2, lower_vnq2, upper_vnq2, precision_vnq2 = stat.confidence_interval_for_variance(var_nq2,
                                                                                                    res[2], 0.95)
        print(f"E[W] = {mean_w}")
        print(f"V(W) = {var_w}")
        print(f"E[Nq] = {mean_nq}")
        print(f"E[Nq]2 = {mean_nq2}")
        print(f"V(Nq) = {var_nq}")
        print(f"V(Nq)2 = {var_nq2}")
        print(f"E[W] CI: Center = {center_ew} lower = {lower_ew} upper = {upper_ew} precision = {precision_ew}")
        print(f"V[W] CI: Center = {center_vw} lower = {lower_vw} upper = {upper_vw} precision = {precision_vw}")
        print(f"E[Nq] CI: Center = {center_enq} lower = {lower_enq} upper = {upper_enq} precision = {precision_enq}")
        print(f"E[Nq]2 CI: Center = {center_enq2} lower = {lower_enq2} upper = {upper_enq2} precision = {precision_enq2}")
        print(f"V[Nq] CI: Center = {center_vnq} lower = {lower_vnq} upper = {upper_vnq} precision = {precision_vnq}")
        print(f"V[Nq]2 CI: Center = {center_vnq2} lower = {lower_vnq2} upper = {upper_vnq2} precision = {precision_vnq2}")
