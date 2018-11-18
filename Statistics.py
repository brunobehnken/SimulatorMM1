from scipy.stats import t, chi2
from math import sqrt


class Statistics:

    @staticmethod
    def calculate_mean(sample):
        """Returns a float with the mean of a sample"""
        return sum(sample) / len(sample)

    @staticmethod
    def calculate_variance(sample, mean):
        """Returns a float with the variance of a sample"""
        variance_sum = 0
        for _sample in sample:
            variance_sum += (_sample - mean) ** 2
        return variance_sum / (len(sample) - 1)

    @staticmethod
    def confidence_interval_for_mean(mean, variance, num_rounds, confidence_interval):
        """Calculates interval of confidence for the mean by the t-Student distribution.
        Returns the center of the interval, the upper and lower bounds and its precision"""
        alpha = 1 - confidence_interval
        alpha /= 2
        t_student = t.isf(alpha, num_rounds - 1)
        mul = sqrt(variance / num_rounds)
        upper = mean + t_student * mul
        lower = mean - t_student * mul
        precision = (upper - lower) / (upper + lower)
        center = (upper + lower)/2

        return center, upper, lower, precision

    @staticmethod
    def confidence_interval_for_variance(variance, num_rounds, confidence_interval):
        """Calculates interval of confidence for the variance by the Chi-square distribution
        Returns the center of the interval, the upper and lower bounds and its precision"""
        alpha_lower = 1 - confidence_interval
        alpha_lower /= 2
        alpha_upper = 1 - alpha_lower
        df = num_rounds - 1
        chi2_lower = chi2.isf(alpha_lower, df)
        chi2_upper = chi2.isf(alpha_upper, df)
        lower = df * variance / chi2_lower
        upper = df * variance / chi2_upper
        precision = (chi2_lower - chi2_upper) / (chi2_lower + chi2_upper)
        center = (upper + lower) / 2

        return center, upper, lower, precision
