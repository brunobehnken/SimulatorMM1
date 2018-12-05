# THIS FILE CONTAINS THE main() FUNCTION FOR RUNNING THE SIMULATOR WITHOUT FLASK
# AS WELL AS THE OLD CALL FOR THIS FUNCTION
from Master import Master


def main(self):
    k = 1_000  # TODO this value is arbitrary for now but must be set later
    discipline = int(input("Type 1 for FCFS or 2 for LCFS (default=FCFS): ") or 1)
    discipline -= 1
    if discipline != 0 and discipline != 1:
        print("invalid input")
        return
    rho = float(input("Insert utilization [0.2] [0.4] [0.6] [0.8] [0.9] (default=[0.2]): ") or 0.2)
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
    for i in range(len(results_w)):
        print(results_w[i])
    for i in range(len(results_nq)):
        print(results_nq[i])


if __name__ == "__main__":
    master = Master()
    master.main()
