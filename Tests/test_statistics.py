from random import random
from unittest import TestCase

from scipy.stats import tmean, tvar, bayes_mvs

from Statistics import Statistics


class TestStatistics(TestCase):

    def setUp(self):
        self.stat = Statistics()

    def test_calculate_mean(self):
        sample = []
        for i in range(0, 100):
            sample.append(random())
        mean = self.stat.calculate_mean(sample)
        control = tmean(sample)
        self.assertAlmostEqual(mean, control)

    def test_calculate_variance(self):
        sample = []
        for i in range(0, 100):
            sample.append(random())
        var = self.stat.calculate_variance(sample, self.stat.calculate_mean(sample))
        control = tvar(sample)
        self.assertAlmostEqual(var, control)

    def test_confidence_interval_for_mean(self):
        n = 100
        sample = []
        for i in range(0, n):
            sample.append(random())
        mean = self.stat.calculate_mean(sample)
        var = self.stat.calculate_variance(sample, mean)
        center, upper, lower, precision = self.stat.confidence_interval_for_mean(mean, var, n, 0.95)
        res = bayes_mvs(sample, 0.95)
        self.assertAlmostEqual(center, res[0][0])
        self.assertAlmostEqual(lower, res[0][1][0])
        self.assertAlmostEqual(upper, res[0][1][1])

    def test_confidence_interval_for_variance(self):
        n = 100
        sample = []
        for i in range(0, n):
            sample.append(random())
        mean = self.stat.calculate_mean(sample)
        var = self.stat.calculate_variance(sample, mean)
        center, upper, lower, precision = self.stat.confidence_interval_for_variance(var, n, 0.95)
        res = bayes_mvs(sample, 0.95)
        self.assertAlmostEqual(lower, res[1][1][0])
        self.assertAlmostEqual(upper, res[1][1][1])
