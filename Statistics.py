from scipy.stats import t, chi2, sqrt


class Statistics:

    # def __calculate_samples_means(self, means):
    #     """Calculate the mean of all rounds means"""
    #     waiting_time_means_sum = 0
    #     areas_means_sum = 0
    #     for mean in means:
    #         waiting_time_means_sum += mean[0]
    #         areas_means_sum += mean[1]
    #
    #     return waiting_time_means_sum / len(means), areas_means_sum / len(means)

    # def __calculate_samples_variances(self, means, waiting_times_mean, areas_mean):
    #     """Calculate the variance of all rounds means"""
    #     waiting_times_variance_sum = 0
    #     areas_variance_sum = 0
    #     for mean in means:
    #         waiting_times_variance_sum += (mean[0] - waiting_times_mean) ** 2
    #         areas_variance_sum += (mean[1] - areas_mean) ** 2
    #
    #     return waiting_times_variance_sum / (len(means) - 1), areas_variance_sum / (len(means) - 1)

    @staticmethod
    def calculate_mean(sample):
        """Calculate the mean of a sample"""
        return sum(sample) / len(sample)

    @staticmethod
    def calculate_variance(sample, mean):
        """Calculate the variance of a sample"""
        variance_sum = 0
        for _sample in sample:
            variance_sum += (_sample - mean) ** 2
        return variance_sum / (len(sample) - 1)

    @staticmethod
    def confidence_interval_for_mean(mean, variance, num_rounds, confidence_interval):
        """Calculates interval of confidence for the mean by the t-Student distribution"""
        alpha = 1 - confidence_interval
        alpha /= 2
        t_student = t.isf(alpha, num_rounds - 1)
        mul = sqrt(variance / num_rounds)
        upper = mean + t_student * mul
        lower = mean - t_student * mul
        # t_student_0975 = 1.960
        # upper = self.__waiting_times_mean + t_student_0975 * (
        #     math.sqrt(self.__waiting_times_variance / self.__number_of_rounds))
        # lower = self.__waiting_times_mean - t_student_0975 * (
        #     math.sqrt(self.__waiting_times_variance / self.__number_of_rounds))
        precision = (upper - lower) / (upper + lower)

        return upper, lower, precision

    @staticmethod
    def confidence_interval_for_variance(variance, num_rounds, confidence_interval):
        """Calculates interval of confidence for the variance by the Chi-square distribution"""
        alpha_lower = 1 - confidence_interval
        alpha_lower /= 2
        alpha_upper = 1 - alpha_lower
        df = num_rounds - 1
        chi2_lower = chi2.isf(alpha_lower, df)
        chi2_upper = chi2.isf(alpha_upper, df)
        lower = df * variance / chi2_lower
        upper = df * variance / chi2_upper
        # chi_square_0975 = 3044.1302
        # chi_square_0025 = 3357.6582
        # upper = ((self.__number_of_rounds - 1) * self.__waiting_times_variance) / chi_square_0975
        # lower = ((self.__number_of_rounds - 1) * self.__waiting_times_variance) / chi_square_0025
        precision = (upper - lower) / (upper + lower)

        return upper, lower, precision

    # def confidence_interval_for_area_mean(self):
    #     """Calculates interval of confidence for the mean
    #     of the graphic's (number of people in line X time) area by the t-Student distribution"""
    #     t_student_0975 = 1.960
    #     upper = self.__areas_mean + t_student_0975 * (math.sqrt(self.__areas_variance / self.__number_of_rounds))
    #     lower = self.__areas_mean - t_student_0975 * (math.sqrt(self.__areas_variance / self.__number_of_rounds))
    #     precision = (upper - lower) / (upper + lower)
    #
    #     return upper, lower, precision
    #
    # def confidence_interval_for_area_variance(self):
    #     """Calculates interval of confidence for the variance
    #     of the graphic's (number of people in line X time) area by the Chi-square distribution"""
    #     chi_square_0975 = 3044.1302
    #     chi_square_0025 = 3357.6582
    #     upper = ((self.__number_of_rounds - 1) * self.__areas_variance) / chi_square_0975
    #     lower = ((self.__number_of_rounds - 1) * self.__areas_variance) / chi_square_0025
    #     precision = (upper - lower) / (upper + lower)
    #
    #     return upper, lower, precision
