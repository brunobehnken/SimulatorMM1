from Simulator import SimulatorFCFS, SimulatorLCFS
from Statistics import Statistics


# noinspection PyPep8Naming
class Master:

    @staticmethod
    def run_FCFS(rho, k):
        """Runs the simulation for FCFS discipline with given parameters,
        returning its statistics"""
        results_w = []
        results_nq = []
        stat_w = Statistics()
        stat_nq = Statistics()
        simulator = SimulatorFCFS(rho)
        simulator.transient_phase()
        for i in range(0, 3200):
            res = simulator.simulate_FCFS(k)
            mean_w = stat_w.calculate_incremental_mean(res[0])
            var_w = stat_w.calculate_incremental_variance(res[0])
            mean_nq = stat_nq.calculate_incremental_time_mean(res[1], res[2])
            var_nq = stat_nq.calculate_incremental_variance(res[1])
            center_ew, lower_ew, upper_ew, precision_ew = stat_w.confidence_interval_for_mean(mean_w, var_w,
                                                                                              len(res[0]), 0.95)
            center_vw, lower_vw, upper_vw, precision_vw = stat_w.confidence_interval_for_variance(var_w, len(res[0]),
                                                                                                  0.95)
            center_enq, lower_enq, upper_enq, precision_enq = stat_nq.confidence_interval_for_mean(mean_nq, var_nq,
                                                                                                   res[2], 0.95)
            center_vnq, lower_vnq, upper_vnq, precision_vnq = stat_nq.confidence_interval_for_variance(var_nq,
                                                                                                       res[2], 0.95)
            results_w.append(((mean_w, center_ew, lower_ew, upper_ew, precision_ew),
                              (var_w, center_vw, lower_vw, upper_vw, precision_vw)))
            results_nq.append(((mean_nq, center_enq, lower_enq, upper_enq, precision_enq),
                               (var_nq, center_vnq, lower_vnq, upper_vnq, precision_vnq)))
        return results_w, results_nq

    @staticmethod
    def run_LCFS(rho, k):
        """Runs the simulation for LCFS discipline with given parameters,
        returning its statistics"""
        results_w = []
        results_nq = []
        stat_w = Statistics()
        stat_nq = Statistics()
        simulator = SimulatorLCFS(rho)
        simulator.transient_phase()
        for i in range(0, 3200):
            res = simulator.simulate_LCFS(k)
            mean_w = stat_w.calculate_incremental_mean(res[0])
            var_w = stat_w.calculate_incremental_variance(res[0])
            mean_nq = stat_nq.calculate_incremental_time_mean(res[1], res[2])
            var_nq = stat_nq.calculate_incremental_variance(res[1])
            center_ew, lower_ew, upper_ew, precision_ew = stat_w.confidence_interval_for_mean(mean_w, var_w,
                                                                                              len(res[0]), 0.95)
            center_vw, lower_vw, upper_vw, precision_vw = stat_w.confidence_interval_for_variance(var_w, len(res[0]),
                                                                                                  0.95)
            center_enq, lower_enq, upper_enq, precision_enq = stat_nq.confidence_interval_for_mean(mean_nq, var_nq,
                                                                                                   res[2], 0.95)
            center_vnq, lower_vnq, upper_vnq, precision_vnq = stat_nq.confidence_interval_for_variance(var_nq,
                                                                                                       res[2], 0.95)
            results_w.append(((mean_w, center_ew, lower_ew, upper_ew, precision_ew),
                              (var_w, center_vw, lower_vw, upper_vw, precision_vw)))
            results_nq.append(((mean_nq, center_enq, lower_enq, upper_enq, precision_enq),
                               (var_nq, center_vnq, lower_vnq, upper_vnq, precision_vnq)))
        return results_w, results_nq

    def webmain(self, discipline, rho):
        """Main function for running the simulator, to be called by Flask front-end.
        Returns the means and variances with all confidence intervals for both
        waiting times and nunber of client at the queue."""
        k = 1_000  # TODO this value is arbitrary for now but must be set later
        # k = 50  # TODO this value is arbitrary for now but must be set later
        discipline -= 1
        if discipline != 0 and discipline != 1:
            print("invalid input")
            return
        if discipline:  # LCFS
            if rho == 0.2 or rho == 0.4 or rho == 0.6 or rho == 0.8 or rho == 0.9:
                print("Simulating...")
                results_w, results_nq = self.run_LCFS(rho, k)
            else:
                print("invalid input")
                return
        else:  # FCFS
            if rho == 0.2 or rho == 0.4 or rho == 0.6 or rho == 0.8 or rho == 0.9:
                print("Simulating...")
                results_w, results_nq = self.run_FCFS(rho, k)
            else:
                print("invalid input")
                return

        w_means = []
        w_means_icl = []
        w_means_icu = []
        w_vars = []
        w_vars_icl = []
        w_vars_icu = []
        nq_means = []
        nq_means_icl = []
        nq_means_icu = []
        nq_vars = []
        nq_vars_icl = []
        nq_vars_icu = []
        results_w = results_w[::10]
        results_nq = results_nq[::10]
        for i in range(len(results_w)):
            w_means.append(results_w[i][0][0])
            w_means_icl.append(results_w[i][0][2])
            w_means_icu.append(results_w[i][0][3])
            w_vars.append(results_w[i][1][0])
            w_vars_icl.append(results_w[i][1][2])
            w_vars_icu.append(results_w[i][1][3])
        for i in range(len(results_nq)):
            nq_means.append(results_nq[i][0][0])
            nq_means_icl.append(results_nq[i][0][2])
            nq_means_icu.append(results_nq[i][0][3])
            nq_vars.append(results_nq[i][1][0])
            nq_vars_icl.append(results_nq[i][1][2])
            nq_vars_icu.append(results_nq[i][1][3])

        return w_means, w_means_icl, w_means_icu, \
            w_vars, w_vars_icl, w_vars_icu, \
            nq_means, nq_means_icl, nq_means_icu, \
            nq_vars, nq_vars_icl, nq_vars_icu
