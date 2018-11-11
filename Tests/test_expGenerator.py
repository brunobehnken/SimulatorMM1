from random import expovariate, seed
from unittest import TestCase

from Generators import ExpGenerator


class TestExpGenerator(TestCase):

    def setUp(self):
        """Settings for lambda, size of the sample, seed for the RNG and precision of comparison"""
        self.lamb = 2
        self.size = 1_000_000
        self.seed = None
        self.precision = 2

    def test_get_exponential_list(self):
        """Builds a list of size self.size using both ExpGenerator.get_exponential_list
        and python's builtin exponential generator method expovariate,
        and compares the results"""
        mean, var, expo_mean, expo_var = 0, 0, 0, 0
        expo = []
        generator = ExpGenerator(self.lamb, self.seed)

        seed(self.seed)
        res = generator.get_exponential_list(self.size)
        for i in range(0, self.size):
            expo.append(expovariate(self.lamb))
        for i in range(0, self.size):
            mean += res[i]
            expo_mean += expo[i]
        mean = mean / self.size
        expo_mean = expo_mean / self.size
        for i in range(0, self.size):
            var += (res[i] - mean) ** 2
            expo_var += (expo[i] - expo_mean) ** 2
        var = var / (self.size - 1)
        expo_var = expo_var / (self.size - 1)

        print("\n")
        print(f"Mean:      {1 / self.lamb} == {mean}")
        print(f"Expo Mean: {1 / self.lamb} == {expo_mean}")
        print(f"Variance:      {1 / (self.lamb ** 2)} == {var}")
        print(f"Expo Variance: {1 / (self.lamb ** 2)} == {expo_var}")
        print("\n")

        self.assertAlmostEqual(abs(mean - expo_mean), 0.0, self.precision)
        self.assertAlmostEqual(abs(var - expo_var), 0.0, self.precision)

    def test_get_exponential_time(self):
        """Builds a list of size self.size using both ExpGenerator.get_exponential_time
        and python's builtin exponential generator method expovariate,
        and compares the results"""
        mean, var, expo_mean, expo_var = 0, 0, 0, 0
        res = []
        expo = []
        generator = ExpGenerator(self.lamb, self.seed)

        seed(self.seed)
        for i in range(0, self.size):
            res.append(generator.get_exponential_time())
            expo.append(expovariate(self.lamb))
        for i in range(0, self.size):
            mean += res[i]
            expo_mean += expo[i]
        mean = mean / self.size
        expo_mean = expo_mean / self.size
        for i in range(0, self.size):
            var += (res[i] - mean) ** 2
            expo_var += (expo[i] - expo_mean) ** 2
        var = var / (self.size - 1)
        expo_var = expo_var / (self.size - 1)

        print(f"Mean:      {1 / self.lamb} == {mean}")
        print(f"Expo Mean: {1 / self.lamb} == {expo_mean}")
        print(f"Variance:      {1 / (self.lamb ** 2)} == {var}")
        print(f"Expo Variance: {1 / (self.lamb ** 2)} == {expo_var}")
        print("\n")

        self.assertAlmostEqual(abs(mean - expo_mean), 0.0, self.precision)
        self.assertAlmostEqual(abs(var - expo_var), 0.0, self.precision)

    def test_get_exponential_time_lambda_1(self):
        """Builds a list of size self.size using both ExpGenerator.get_exponential_time_lambda1
        and python's builtin exponential generator method expovariate,
        and compares the results"""
        mean, var, expo_mean, expo_var = 0, 0, 0, 0
        res = []
        expo = []
        generator = ExpGenerator(1, self.seed)

        seed(self.seed)
        for i in range(0, self.size):
            res.append(generator.get_exponential_time_lambda_1())
            expo.append(expovariate(1))
        for i in range(0, self.size):
            mean += res[i]
            expo_mean += expo[i]
        mean = mean / self.size
        expo_mean = expo_mean / self.size
        for i in range(0, self.size):
            var += (res[i] - mean) ** 2
            expo_var += (expo[i] - expo_mean) ** 2
        var = var / (self.size - 1)
        expo_var = expo_var / (self.size - 1)

        print(f"Mean:      1 == {mean}")
        print(f"Expo Mean: 1 == {expo_mean}")
        print(f"Variance:      1 == {var}")
        print(f"Expo Variance: 1 == {expo_var}")

        self.assertAlmostEqual(abs(mean - expo_mean), 0.0, self.precision)
        self.assertAlmostEqual(abs(var - expo_var), 0.0, self.precision)
