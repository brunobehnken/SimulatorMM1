from unittest import TestCase

from Master import Master


class TestMaster(TestCase):
    def test_webmain(self):
        master = Master()
        results_w, results_w_vars, results_nq, results_nq_vars = master.webmain(1, 0.2)
        print(len(results_w))
        print(results_w)

    def test_run_FCFS(self):
        master = Master()
        results_w, results_nq = master.run_FCFS(0.2, 50)
        results_w = results_w[::10]
        print(len(results_w))
        print(results_w[0])
        # print(teste[0][0][0])
