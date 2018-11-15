from Scheduler import Scheduler


class Simulator:

    def __init__(self):
        # TODO these variables may be best placed inside the methods (as class variables, may cause unexpected bugs)
        self.__current_time = 0
        self.__waiting_times = []

    # noinspection PyPep8Naming
    def simulate_FCFS(self, param_lambda, client_num=10):
        # TODO change documentation
        """Runs one sample of the FCFS queue with arrival rate 'param_lambda', collecting statistics"""

        # client_num = 10  # TODO this should be passed as a parameter, remove this line (?)
        counter = 1  # Counter of arrivals. Starts as 1 because the scheduler schedules the 1st arrival automatically
        queue = []
        server_idle = True
        scheduler = Scheduler(param_lambda)

        # Start Simulation
        next_event = scheduler.get_next_event()
        while next_event is not None:
            client = next_event[1]
            if next_event[0] == 'a':
                # TODO find a way to hold last current time for queue graphic area calculus purposes
                self.__current_time = client.get_arrival_time()  # set current time to arrival time
                if server_idle:
                    client.set_wait_time(0)
                    self.__waiting_times.append(client.get_wait_time())  # TODO append list of waiting times
                    client.set_departure_time(client.get_arrival_time() + client.get_wait_time() +
                                              client.get_service_time())
                    scheduler.schedule_departure(client)
                    server_idle = False
                else:  # if server is busy
                    if queue:  # if queue is not empty, gather 'number of waiting costumers' statistics
                        pass  # TODO calculate area under queue graphic
                    queue.append(client)
                if counter < client_num:  # if necessary, schedule next arrival and update counter
                    scheduler.schedule_next_arrival()
                    counter += 1
            else:
                # TODO find a way to hold last current time for queue graphic area calculus purposes
                self.__current_time = client.get_departure_time()  # set current time to departure time
                del client  # client has departed (:
                if queue:
                    # TODO calculate area under queue graphic
                    client = queue.pop(0)
                    client.set_wait_time(self.__current_time - client.get_arrival_time())
                    self.__waiting_times.append(client.get_wait_time())  # TODO append list of waiting times
                    client.set_departure_time(client.get_arrival_time() + client.get_wait_time() +
                                              client.get_service_time())
                    scheduler.schedule_departure(client)
                else:
                    server_idle = True  # if there is no next client, idle until next arrival
            next_event = scheduler.get_next_event()
        return self.__waiting_times
