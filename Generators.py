from random import seed, random
from math import log


class ExpGenerator:

    def __init__(self, param_lambda=1, input_seed=None):
        self.__lambda = param_lambda
        seed(input_seed)

    def get_lambda(self):
        return self.__lambda

    def set_lambda(self, param_lambda):
        self.__lambda = param_lambda

    @staticmethod
    def set_seed(input_seed):
        seed(input_seed)

    def get_exponential_time(self):
        sample = random()
        time = -1 * (1 / self.__lambda) * log(sample)
        return time

    def get_exponential_list(self, size):
        time = []
        for i in range(0, size):
            sample = random()
            res = -1 * (1 / self.__lambda) * log(sample)
            time.append(res)
        return time

    @staticmethod
    def get_exponential_time_lambda_1():
        sample = random()
        time = -1 * log(sample)
        return time
