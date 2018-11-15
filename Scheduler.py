from Client import Client
from Generators import ExpGenerator


class Scheduler:
    """This class implements a scheduler, which function is to manage
    time-ordered events that will take place in the simulator"""

    def __init__(self, num_clients, param_lambda, seed=None):
        """Starts the scheduler and schedules the first arrival.
        'num_clients' is the total number of clients that will be scheduled.
        'param_lambda' and 'seed' are used to generate exponential times"""

        self.__num_clients = num_clients
        self.__gen = ExpGenerator(param_lambda, seed)
        self.__client_counter = 0  # clients that have already arrived
        self.__last_arrival_time = 0

        # schedule is a time-ordered list of events that are represented as tuples.
        # Each tuple has 3 elements: the first is either 'a' (for an arrival event) or 'd' (for a departure event).
        # The second element is the time the event will take place (for simplicity of implementation only).
        # The third element is an instance of Client that represents
        # the client that will arrive to or departure from the system.
        self.__schedule = []

        # schedule first arrival
        client = Client(0, self.__gen.get_exponential_time_lambda_1())
        # self.__schedule.append(('a', 0, client))  # updates the schedule
        self.__update_schedule(('a', client))
        self.__client_counter += 1

    def __schedule_next_arrival(self):
        """Schedule the event of the next client arrival, if possible"""
        if self.__client_counter == self.__num_clients:  # if all the clients have already arrived, return
            return
        self.__last_arrival_time += self.__gen.get_exponential_time()  # calculate next arrival time
        client = Client(self.__last_arrival_time, self.__gen.get_exponential_time_lambda_1())
        self.__update_schedule(('a', client))
        self.__client_counter += 1

    def schedule_departure(self, client):
        """Schedule the event of the departure of the client currently being served"""
        self.__update_schedule(('d', client))

    def __update_schedule(self, event):
        """Updates the schedule with the event, preserving time-ordering"""
        i = 0
        size = len(self.__schedule)
        if event[0] == 'a':
            time = event[1].get_arrival_time()
            # seeks the right position to add the event to the schedule
            while i < size and self.__schedule[i][1] < time:
                i += 1
            self.__schedule.insert(i, ('a', time, event[1]))
        else:
            time = event[1].get_departure_time()
            # seeks the right position to add the event to the schedule
            while i < size and self.__schedule[i][1] < time:
                i += 1
            self.__schedule.insert(i, ('d', time, event[1]))

    def get_next_event(self):
        """Returns the next event in the schedule or None if the schedule is empty.
        Automatically schedules the next arrival if necessary"""
        if len(self.__schedule) == 0:
            return None
        event = self.__schedule.pop(0)
        if event[0] == 'a':
            self.__schedule_next_arrival()
        tup = (event[0], event[2])
        return tup
