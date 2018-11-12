from random import seed, random
from math import log


class ExpGenerator:
    """This class implements sample generators for the exponential distribution"""

    def __init__(self, param_lambda=1, input_seed=None):
        """Sets the lambda to be used by the generator
        and the seed to be used by the RNG"""
        self.__lambda = param_lambda
        seed(input_seed)

    def get_lambda(self):
        """Returns the current value of lambda"""
        return self.__lambda

    def set_lambda(self, param_lambda):
        """Set the value of lambda"""
        self.__lambda = param_lambda

    @staticmethod
    def set_seed(input_seed):
        """Set a new seed to be used by the RNG"""
        seed(input_seed)

    def get_exponential_time(self):
        """Returns a sample time of the exponential
        distribution using the current lambda"""
        sample = random()
        time = -1 * (1 / self.__lambda) * log(sample)
        return time

    def get_exponential_list(self, size):
        """Returns a list of size 'size' of sample times of
        the exponential distribution using the current lambda"""
        time = []
        for i in range(0, size):
            sample = random()
            res = -1 * (1 / self.__lambda) * log(sample)
            time.append(res)
        return time

    @staticmethod
    def get_exponential_time_lambda_1():
        """Returns a sample time of the exponential
        distribution using lambda = 1"""
        sample = random()
        time = -1 * log(sample)
        return time
