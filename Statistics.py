from scipy.stats import t, chi2
from math import sqrt


class Statistics:

    def __init__(self):
        self.__mean_sample_sum = 0
        self.__mean_num_sample = 0
        self.__var_sample_sum = 0
        self.__var_sample_sum_of_squares = 0
        self.__var_num_sample = 0

    @staticmethod
    def calculate_mean(sample):
        """Returns a float with the mean of a sample"""
        return sum(sample) / len(sample)

    def calculate_incremental_mean(self, sample):
        """Returns a float with the mean of all the samples given until now.
        Values can be reset using the reset method."""
        self.__mean_sample_sum += sum(sample)
        self.__mean_num_sample += len(sample)
        return self.__mean_sample_sum / self.__mean_num_sample

    @staticmethod
    def calculate_variance(sample, mean):
        """Returns a float with the variance of a sample"""
        variance_sum = 0
        for _sample in sample:
            variance_sum += (_sample - mean) ** 2
        return variance_sum / (len(sample) - 1)

    def calculate_incremental_variance(self, sample):
        """Returns a float with the variance of all the samples given until now.
        Values can be reset using the reset method."""
        self.__var_sample_sum += sum(sample)
        self.__var_num_sample += len(sample)
        for i in range(0, len(sample)):
            self.__var_sample_sum_of_squares += sample[i] ** 2
        return (self.__var_sample_sum_of_squares / (self.__var_num_sample - 1))\
            - (self.__var_sample_sum ** 2 / (self.__var_num_sample * (self.__var_num_sample - 1)))

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
        return center, lower, upper, precision

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
        return center, lower, upper, precision

    def reset(self):
        """This method resets the metrics for incremental calculus of mean and variance"""
        self.__mean_sample_sum = 0
        self.__mean_num_sample = 0
        self.__var_sample_sum = 0
        self.__var_sample_sum_of_squares = 0
        self.__var_num_sample = 0
