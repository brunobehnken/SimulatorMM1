from Scheduler import Scheduler
from Statistics import Statistics


class SimulatorFCFS:
    """This class implements a FCFS queue simulator, which function is
    to gather statistics for this discipline of service"""

    def __init__(self, rho, seed=None):
        """Starts the simulator using 'rho' as its utilization.
        This parameter cannot be changed later"""
        self.__rho = rho
        self.__start_time = 0  # start_time of simulation rounds
        self.__current_time = 0  # current time of the simulator (state variable kept over function calls)
        self.__queue = []  # queue of the simulator (state variable kept over function calls)
        self.__server_idle = True  # state of the server of the simulator (state variable kept over function calls)
        self.__scheduler = Scheduler(rho, seed)  # Scheduler (state variable kept over function calls)
        self.__waiting_times = []  # list of waiting times of the costumers, for statistics
        self.__areas = []  # list of number of waiting costumers, for statistics

    # noinspection PyPep8Naming
    def simulate_FCFS(self, client_num):
        """Runs the simulation of a FCFS queue until 'client_num' statistics are gathered,
        when the simulation is paused. The state of the simulation is kept to be used on future
        calls. Statistics are only relevant after transient phase has passed."""

        counter = 0  # Counter of wait_time statistics gathered
        self.__start_time = self.__current_time  # start_time of this simulation round

        # Start Simulation
        next_event = self.__scheduler.get_next_event()  # next scheduled event
        while True:  # keep simulating until break (when the necessary statistics are gathered)
            client = next_event[1]  # client of the event being treated
            if next_event[0] == 'a':  # if the event is an arrival
                delta_time = self.__current_time  # updates delta_time for statistics purposes
                self.__current_time = client.get_arrival_time()  # set current time to arrival time
                if self.__server_idle:  # if server is idle, client gets served immediately
                    client.set_wait_time(0)  # no wait_time at all
                    self.__areas.append(0)  # updates 'waiting costumers' statistics with 0 waiting costumers
                    self.__waiting_times.append(client.get_wait_time())  # updates wait_time statistics
                    counter += 1  # Increments counter of wait_time statistics gathered
                    client.set_departure_time(client.get_arrival_time() + client.get_wait_time() +
                                              client.get_service_time())  # calculates departure time
                    self.__scheduler.schedule_departure(client)  # schedule client departure event
                    self.__server_idle = False  # server is now busy serving the client
                else:  # if server is busy, client goes to the queue
                    if self.__queue:  # if queue is not empty, updates 'waiting costumers' statistics
                        delta_time -= self.__current_time  # calculates the amount of time
                        delta_time *= -1  # fix delta_time sign
                        area = delta_time * len(self.__queue)  # calculates the area under the graphic
                        self.__areas.append(area)  # updates 'waiting costumers' statistics
                    self.__queue.append(client)  # client goes to the queue
                self.__scheduler.schedule_next_arrival(0)  # schedule next arrival  # TODO implement round number
                if counter == client_num:  # if the requested statistics were gathered, pause simulation
                    break  # ATTENTION: simulation should NOT break before schedule_next_arrival()

            else:  # if the event is a departure
                delta_time = self.__current_time  # updates delta_time for statistics purposes
                self.__current_time = client.get_departure_time()  # set current time to departure time
                del client  # client has departed (:
                if self.__queue:  # if queue is not empty, serve next client
                    delta_time -= self.__current_time  # calculates the amount of time
                    delta_time *= -1  # fix delta_time sign
                    area = delta_time * len(self.__queue)  # calculates the area under the graphic
                    self.__areas.append(area)  # updates 'waiting costumers' statistics
                    client = self.__queue.pop(0)  # call the next client using FCFS discipline
                    client.set_wait_time(self.__current_time - client.get_arrival_time())  # calculates the wait_time
                    self.__waiting_times.append(client.get_wait_time())  # updates wait_time statistics
                    counter += 1  # Increments counter of wait_time statistics gathered
                    client.set_departure_time(client.get_arrival_time() + client.get_wait_time() +
                                              client.get_service_time())  # calculates departure time
                    self.__scheduler.schedule_departure(client)  # schedule client departure event
                    if counter == client_num:  # if the requested statistics were gathered, pause simulation
                        break
                else:  # if there is no next client, idle until next arrival
                    self.__server_idle = True
            next_event = self.__scheduler.get_next_event()  # next scheduled event

        final_waiting_times = self.__waiting_times[:]  # creates copy of waiting_times list to return
        self.__waiting_times.clear()  # clears the waiting_times list for next simulation round
        final_areas = self.__areas[:]  # creates copy of areas list to return
        self.__areas.clear()  # clears the areas list for next simulation round
        round_runtime = self.__current_time - self.__start_time  # calculates amount of time of this simulation round
        res = (final_waiting_times, final_areas, round_runtime)  # builds the return tuple
        return res

    def transient_phase(self):
        """Runs the simulator until the transient phase is finished, which occurs
        when 'chunk_size' variance values under 'threshold' precision are found"""
        stats = Statistics()
        means_w = []
        var = []
        count = 0

        # threshold adjustment
        if self.__rho == 0.2 or self.__rho == 0.4:
            threshold = 0.001
        elif self.__rho == 0.6:
            threshold = 0.01
        elif self.__rho == 0.8:
            threshold = 0.5
        else:
            threshold = 1.0
        chunk_size = 10

        while True:
            # calculate next variance for the variance list
            for i in range(0, 10):
                res = self.simulate_FCFS(100)
                means_w.append(stats.calculate_mean(res[0]))
            var_w = stats.calculate_incremental_variance(means_w)
            means_w.clear()

            if not var:  # if variance list is empty
                var.append(var_w)
                continue

            for i in range(0, len(var)):
                if abs(var_w - var[i]) < threshold:
                    count += 1
            if count == len(var):  # if we found a number in the list threshold, append
                var.append(var_w)
                if len(var) == chunk_size:  # if the list has all members in the threshold, end of transient phase
                    return
            else:  # if the member is not in the list threshold, discart list
                var.clear()
            count = 0  # reset count


class SimulatorLCFS:
    """This class implements a LCFS queue simulator, which function is
    to gather statistics for this discipline of service"""

    def __init__(self, rho, seed=None):
        """Starts the simulator using 'rho' as its utilization.
        This parameter cannot be changed later"""
        self.__rho = rho
        self.__start_time = 0  # start_time of simulation rounds
        self.__current_time = 0  # current time of the simulator (state variable kept over function calls)
        self.__queue = []  # queue of the simulator (state variable kept over function calls)
        self.__server_idle = True  # state of the server of the simulator (state variable kept over function calls)
        self.__scheduler = Scheduler(rho, seed)  # Scheduler (state variable kept over function calls)
        self.__waiting_times = []  # list of waiting times of the costumers, for statistics
        self.__areas = []  # list of number of waiting costumers, for statistics

    # noinspection PyPep8Naming
    def simulate_LCFS(self, client_num):
        """Runs the simulation of a LCFS queue until 'client_num' statistics are gathered,
        when the simulation is paused. The state of the simulation is kept to be used on future
        calls. Statistics are only relevant after transient phase has passed."""

        counter = 0  # Counter of wait_time statistics gathered
        self.__start_time = self.__current_time  # start_time of this simulation round

        # Start Simulation
        next_event = self.__scheduler.get_next_event()  # next scheduled event
        while True:  # keep simulating until break (when the necessary statistics are gathered)
            client = next_event[1]  # client of the event being treated
            if next_event[0] == 'a':  # if the event is an arrival
                delta_time = self.__current_time  # updates delta_time for statistics purposes
                self.__current_time = client.get_arrival_time()  # set current time to arrival time
                if self.__server_idle:  # if server is idle, client gets served immediately
                    client.set_wait_time(0)  # no wait_time at all
                    self.__areas.append(0)  # updates 'waiting costumers' statistics with 0 waiting costumers
                    self.__waiting_times.append(client.get_wait_time())  # updates wait_time statistics
                    counter += 1  # Increments counter of wait_time statistics gathered
                    client.set_departure_time(client.get_arrival_time() + client.get_wait_time() +
                                              client.get_service_time())  # calculates departure time
                    self.__scheduler.schedule_departure(client)  # schedule client departure event
                    self.__server_idle = False  # server is now busy serving the client
                else:  # if server is busy, client goes to the queue
                    if self.__queue:  # if queue is not empty, updates 'waiting costumers' statistics
                        delta_time -= self.__current_time  # calculates the amount of time
                        delta_time *= -1  # fix delta_time sign
                        area = delta_time * len(self.__queue)  # calculates the area under the graphic
                        self.__areas.append(area)  # updates 'waiting costumers' statistics
                    self.__queue.append(client)  # client goes to the queue
                self.__scheduler.schedule_next_arrival(0)  # schedule next arrival  # TODO implement round number
                if counter == client_num:  # if the requested statistics were gathered, pause simulation
                    break  # ATTENTION: simulation should NOT break before schedule_next_arrival()

            else:  # if the event is a departure
                delta_time = self.__current_time  # updates delta_time for statistics purposes
                self.__current_time = client.get_departure_time()  # set current time to departure time
                del client  # client has departed (:
                if self.__queue:  # if queue is not empty, serve next client
                    delta_time -= self.__current_time  # calculates the amount of time
                    delta_time *= -1  # fix delta_time sign
                    area = delta_time * len(self.__queue)  # calculates the area under the graphic
                    self.__areas.append(area)  # updates 'waiting costumers' statistics
                    client = self.__queue.pop()  # call the next client using LCFS discipline
                    client.set_wait_time(self.__current_time - client.get_arrival_time())  # calculates the wait_time
                    self.__waiting_times.append(client.get_wait_time())  # updates wait_time statistics
                    counter += 1  # Increments counter of wait_time statistics gathered
                    client.set_departure_time(client.get_arrival_time() + client.get_wait_time() +
                                              client.get_service_time())  # calculates departure time
                    self.__scheduler.schedule_departure(client)  # schedule client departure event
                    if counter == client_num:  # if the requested statistics were gathered, pause simulation
                        break
                else:  # if there is no next client, idle until next arrival
                    self.__server_idle = True
            next_event = self.__scheduler.get_next_event()  # next scheduled event

        final_waiting_times = self.__waiting_times[:]  # creates copy of waiting_times list to return
        self.__waiting_times.clear()  # clears the waiting_times list for next simulation round
        final_areas = self.__areas[:]  # creates copy of areas list to return
        self.__areas.clear()  # clears the areas list for next simulation round
        round_runtime = self.__current_time - self.__start_time  # calculates amount of time of this simulation round
        res = (final_waiting_times, final_areas, round_runtime)  # builds the return tuple
        return res

    def transient_phase(self):
        """Runs the simulator until the transient phase is finished, which occurs
        when 'chunk_size' variance values under 'threshold' precision are found"""
        stats = Statistics()
        means_w = []
        var = []
        count = 0

        # threshold adjustment
        if self.__rho == 0.2 or self.__rho == 0.4:
            threshold = 0.001
        elif self.__rho == 0.6:
            threshold = 0.01
        elif self.__rho == 0.8:
            threshold = 0.5
        else:
            threshold = 1.0
        chunk_size = 10

        while True:
            # calculate next variance for the variance list
            for i in range(0, 10):
                res = self.simulate_LCFS(100)
                means_w.append(stats.calculate_mean(res[0]))
            var_w = stats.calculate_incremental_variance(means_w)
            means_w.clear()

            if not var:  # if variance list is empty
                var.append(var_w)
                continue

            for i in range(0, len(var)):
                if abs(var_w - var[i]) < threshold:
                    count += 1
            if count == len(var):  # if we found a number in the list threshold, append
                var.append(var_w)
                if len(var) == chunk_size:  # if the list has all members in the threshold, end of transient phase
                    return
            else:  # if the member is not in the list threshold, discart list
                var.clear()
            count = 0  # reset count
