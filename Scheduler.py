from Client import Client
from Generators import ExpGenerator


class Scheduler:

    def __init__(self):
        self.__queue = []

    def build_queue(self, size, param_lambda=2, seed=None):
        gen = ExpGenerator(param_lambda, seed)
        arrival_time = 0
        self.__queue.append(Client(arrival_time, gen.get_exponential_time_lambda_1()))
        for i in range(0, size):
            arrival_time += gen.get_exponential_time()
            self.__queue.append(Client(arrival_time, gen.get_exponential_time_lambda_1()))

    def get_queue(self):
        return self.__queue
