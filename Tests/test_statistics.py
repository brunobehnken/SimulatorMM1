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

    def test_calculate_incremental_mean(self):
        control_sample = []
        sample = []
        mean = 0
        for i in range(0, 20):
            for _ in range(0, 100):
                elem = random()
                sample.append(elem)
                control_sample.append(elem)
            mean = self.stat.calculate_incremental_mean(sample)
            sample.clear()
        control = tmean(control_sample)
        self.assertAlmostEqual(mean, control)

    def test_calculate_variance(self):
        sample = []
        for i in range(0, 100):
            sample.append(random())
        var = self.stat.calculate_variance(sample, self.stat.calculate_mean(sample))
        control = tvar(sample)
        self.assertAlmostEqual(var, control)

    def test_calculate_incremental_variance(self):
        control_sample = []
        sample = []
        var = 0
        for i in range(0, 20):
            for _ in range(0, 100):
                elem = random()
                sample.append(elem)
                control_sample.append(elem)
            var = self.stat.calculate_incremental_variance(sample)
            sample.clear()
        control = tvar(control_sample)
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
