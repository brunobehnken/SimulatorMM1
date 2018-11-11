from unittest import TestCase

from Generators import ExpGenerator


class TestExpGenerator(TestCase):

    def test_get_exponential_list(self):
        lamb = 2
        mean = 0
        var = 0
        size = 1_000_000
        generator = ExpGenerator(lamb)
        res = generator.get_exponential_list(size)
        for i in range(0, size):
            mean += res[i]
        mean = mean / size
        for i in range(0, size):
            var += (res[i] - mean) ** 2
        var = var / (size - 1)

        print(f"Mean: {1 / lamb} == {mean}")
        print(f"Variance: {1 / (lamb ** 2)} == {var}")

    def test_get_exponential_time(self):
        lamb = 2
        mean = 0
        var = 0
        size = 1_000_000
        res = []
        generator = ExpGenerator(lamb)
        for i in range(0, size):
            res.append(generator.get_exponential_time())
        for i in range(0, size):
            mean += res[i]
        mean = mean / size
        for i in range(0, size):
            var += (res[i] - mean) ** 2
        var = var / (size - 1)

        print(f"Mean: {1 / lamb} == {mean}")
        print(f"Variance: {1 / (lamb ** 2)} == {var}")

    def test_get_exponential_time_lambda_1(self):
        mean = 0
        var = 0
        size = 1_000_000
        res = []
        generator = ExpGenerator()
        for i in range(0, size):
            res.append(generator.get_exponential_time_lambda_1())
        for i in range(0, size):
            mean += res[i]
        mean = mean / size
        for i in range(0, size):
            var += (res[i] - mean) ** 2
        var = var / (size - 1)

        print(f"Mean: 1 == {mean}")
        print(f"Variance: 1 == {var}")