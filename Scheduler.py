from Client import Client
from Generators import ExpGenerator


class Scheduler:
    """This class implements a scheduler, which function is to generate
    clients and build a queue with them to be passed to the server"""

    def __init__(self):
        """Starts the queue with no clients"""
        self.__queue = []

    def build_queue(self, size, start_time, param_lambda, start_flag=False, seed=None):
        """Generates a queue with 'size' clients that starts at 'start_time' if 'start_flag' is True
        and starts at 'start_time + exponential_time' if 'start_flag' is False.
        Each client has its times generated using the parameters 'param_lambda' and 'seed'"""
        gen = ExpGenerator(param_lambda, seed)
        if start_flag:
            for i in range(0, size):
                self.__queue.append(Client(start_time, gen.get_exponential_time_lambda_1()))
                start_time += gen.get_exponential_time()
        else:
            for i in range(0, size):
                start_time += gen.get_exponential_time()
                self.__queue.append(Client(start_time, gen.get_exponential_time_lambda_1()))

    def get_queue(self):
        """Returns the current queue"""
        return self.__queue

    def empty_queue(self):
        """Deletes the current queue and creates a new empty one"""
        del self.__queue
        self.__queue = []
