from Simulator import SimulatorFCFS, SimulatorLCFS
import math
import time

class Analysis:

	def __init__(self, number_of_rounds, transient_phase_length, rho):
		self.__number_of_rounds = number_of_rounds
		self.__transient_phase_length = transient_phase_length
		self.simulator = SimulatorFCFS(rho)
		self.__waiting_times_mean = None
		self.__areas_mean = None
		self.__waiting_times_variance = None
		self.__areas_variance = None
		self.__best_k_value = None

	def __transient_phase(self):
		self.simulator.simulate_FCFS(self.__transient_phase_length)

	def __calculate_round_means(self, k):
		stats = self.simulator.simulate_FCFS(k)
		waiting_times = stats[0]
		areas = stats[1][:k]
		return [sum(waiting_times)/len(waiting_times), sum(areas)/len(areas)]

	def __calculate_samples_means(self, means):
		"""Calculate the mean of all rounds means"""
		waiting_time_means_sum = 0
		areas_means_sum = 0
		for mean in means:
			waiting_time_means_sum += mean[0]
			areas_means_sum += mean[1]

		return waiting_time_means_sum/len(means), areas_means_sum/len(means)

	def __calculate_samples_variances(self, means, wainting_times_mean, areas_mean):
		"""Calculate the variance of all rounds means"""
		waiting_times_variance_sum = 0
		areas_variance_sum = 0
		for mean in means:
			waiting_times_variance_sum += (mean[0] - wainting_times_mean)**2
			areas_variance_sum += (mean[1] - areas_mean)**2

		return waiting_times_variance_sum/(len(means) - 1), areas_variance_sum/(len(means) - 1)

	def set_best_k_value(self, initial_k, k_rounds):
		"""Gets the best value for k(number of samples collected in a round of the Batch method)
		through calculating the covariance of successive rounds for a certain k and getting 
		the one that comes closer to the variance. Every iteration k is doubled"""

		k = initial_k
		var_cov_ratio = None
		covariance = None

		rounds_means = [] # list of round's means(waiting time mean and area mean)
		for _ in range(k_rounds):
			print("k: ", k)
			self.__transient_phase()
			for _round in range(self.__number_of_rounds):
				rounds_means.append(self.__calculate_round_means(k)) # appends round mean to the list of round's means
			print("rounds_means: ", len(rounds_means))
			wainting_times_mean, areas_mean = self.__calculate_samples_means(rounds_means) # gets the mean of all rounds means for k smaples per round
			wainting_times_variance, areas_variance = self.__calculate_samples_variances(rounds_means, wainting_times_mean, areas_mean) # gets the variance of all rounds means for k smaples per round

			cov_sum = 0
			for j in range(self.__number_of_rounds - 1):
				cov_sum += (rounds_means[j][0] - wainting_times_mean)*(rounds_means[j + 1][0] - wainting_times_mean)
			covariance = cov_sum/(self.__number_of_rounds - 2)
			new_var_cov_ratio = abs(wainting_times_variance/covariance)
			print("variance: ", wainting_times_variance)
			print("covariance: ", covariance)
			print("new: ", new_var_cov_ratio)
			print("old: ", var_cov_ratio)
			if(var_cov_ratio is None):
				print(new_var_cov_ratio)
				var_cov_ratio = new_var_cov_ratio
				self.__best_k_value = k
			elif(new_var_cov_ratio > var_cov_ratio):
				print(new_var_cov_ratio)
				var_cov_ratio = new_var_cov_ratio
				self.__best_k_value = k

			k *= 2

	def set_stats_for_best_k_value(self):
		"""Sets the mean and variance of the waiting time in line and area of graphic(number of people in line X time) of all rounds.
		Each round having k samples collected, with the best value of k calulated in the function set_best_k_value(self, initial_k, k_rounds)"""		
		self.__transient_phase()
		rounds_means = []
		for _round in range(self.__number_of_rounds):
			rounds_means.append(self.__calculate_round_means(self.__best_k_value))
		self.__waiting_times_mean, self.__areas_mean = self.__calculate_samples_means(rounds_means)
		self.__waiting_times_variance, self.__areas_variance = self.__calculate_samples_variances(rounds_means, self.__waiting_times_mean, self.__areas_mean)

	def confidence_interval_for_waiting_time_mean(self):
		"""Calculates interval of confidence for the mean of the waiting time in line by the t-Student distribution"""
		t_student_0975 = 1.960
		U = self.__waiting_times_mean + t_student_0975*(math.sqrt(self.__waiting_times_variance/self.__number_of_rounds))
		L = self.__waiting_times_mean - t_student_0975*(math.sqrt(self.__waiting_times_variance/self.__number_of_rounds))
		precision = (U - L)/(U + L)

		return U, L, precision

	def confidence_interval_for_waiting_time_variance(self):
		"""Calculates interval of confidence for the variance of the waiting time in line by the Chi-square distribution"""
		chi_square_0975 = 3044.1302
		chi_square_0025 = 3357.6582
		U = ((self.__number_of_rounds - 1)*self.__waiting_times_variance)/chi_square_0975
		L = ((self.__number_of_rounds - 1)*self.__waiting_times_variance)/chi_square_0025
		precision = (U - L)/(U + L)

		return U, L, precision

	def confidence_interval_for_area_mean(self):
		"""Calculates interval of confidence for the mean of the graphic's(number of people in line X time) area by the t-Student distribution"""
		t_student_0975 = 1.960
		U = self.__areas_mean + t_student_0975*(math.sqrt(self.__areas_variance/self.__number_of_rounds))
		L = self.__areas_mean - t_student_0975*(math.sqrt(self.__areas_variance/self.__number_of_rounds))
		precision = (U - L)/(U + L)

		return U, L, precision

	def confidence_interval_for_area_variance(self):
		"""Calculates interval of confidence for the variance of the graphic's(number of people in line X time) area by the Chi-square distribution"""
		chi_square_0975 = 3044.1302
		chi_square_0025 = 3357.6582
		U = ((self.__number_of_rounds - 1)*self.__areas_variance)/chi_square_0975
		L = ((self.__number_of_rounds - 1)*self.__areas_variance)/chi_square_0025
		precision = (U - L)/(U + L)

		return U, L, precision

start = time.time()

analizer = Analysis(number_of_rounds = 3200, transient_phase_length = 100, rho = 0.8)
analizer.set_best_k_value(10, 10)
analizer.set_stats_for_best_k_value()
print(analizer.confidence_interval_for_waiting_time_mean())
print(analizer.confidence_interval_for_waiting_time_variance())
print(analizer.confidence_interval_for_area_mean())
print(analizer.confidence_interval_for_area_variance())

finish = time.time() - start
print("runtime: " + str(round(finish/60, 2)) + " min")