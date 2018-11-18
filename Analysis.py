from Simulator import SimulatorFCFS, SimulatorLCFS
import math
import time

class Analysis:

	def __init__(self, number_of_rounds, transient_phase_length, rho):
		self.__number_of_rounds = number_of_rounds
		self.__transient_phase_length = transient_phase_length
		self.__simulator = SimulatorFCFS(rho)
		self.__waiting_times_mean = None
		self.__areas_mean = None
		self.__waiting_times_variance = None
		self.__areas_variance = None
		self.__best_k_value = None

	def get_simulator(self):
		return self.__simulator

	def get_k(self):
		return self.__best_k_value

	def set_k(self, k):
		self.__best_k_value = k

	def __transient_phase(self):
		self.__simulator.simulate_FCFS(self.__transient_phase_length)

	def __calculate_round_means(self, k):
		stats = self.__simulator.simulate_FCFS(k)
		# print(stats)
		waiting_times = stats[0]
		areas = stats[1][:k]
		if(areas == []):
			print(stats)
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

		for _ in range(k_rounds):
			rounds_means = [] # list of round's means(waiting time mean and area mean)
			print("k: ", k)
			self.__transient_phase()
			for _round in range(self.__number_of_rounds):
				if(_round%500 == 0):
					print("Round: " + str(_round) + "   K : " + str(k))
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

def transient_phase_analysis():
	analizer = Analysis(number_of_rounds = 3200, transient_phase_length = 100, rho = 0.8)
	simulator = analizer.get_simulator()
	c2 = 0
	consecutives = 0
	consecutives_between = 0
	sizes = []
	sizes_between = []
	lowest_variance = 10
	for r in range(10):
		res = simulator.simulate_FCFS(100000)
		last = []
		var_sum = 0
		c = 0
		last_was_less_than_lowest_variance = False
		for i in res[1]:
			last.append(i)
			if(len(last) > 1000):
				last.pop(0)
				mean = sum(last)/1000
				for e in last:
					var_sum += (e - mean)**2
				variance = var_sum/(1000 - 1)
				var_sum = 0
				if(variance <= lowest_variance):
					if(last_was_less_than_lowest_variance == True):
						consecutives += 1
					else:
						if(consecutives_between > 0):
							sizes_between.append(consecutives_between)
							consecutives_between = 0
					last_was_less_than_lowest_variance = True
				else:
					if(last_was_less_than_lowest_variance == True):
						if(consecutives > 0):
							c2 += 1
							sizes.append(consecutives)
							consecutives = 0
					else:
						consecutives_between += 1
					last_was_less_than_lowest_variance = False

			c += 1
		consecutives = 0
		consecutives_between = 0
		if(len(sizes) > 0):
			print("count: " + str(c2) + "  size mean: " + str(sum(sizes)/len(sizes)))
		else:
			print("no equilibrium this time")
		if(len(sizes_between) > 0):
			print("size between mean: ", sum(sizes_between)/len(sizes_between))
		elif(not(len(sizes_between) > 0) and not(len(sizes) > 0)):
			print("no equilibrium this time")
		else:
			print("always on equilibrium") # this will porbably never happen
		sizes = []
		sizes_between = []
		c2 = 0

def set_best_k_for_variance():
	analizer = Analysis(number_of_rounds = 3200, transient_phase_length = 30000, rho = 0.8)

	analizer.set_best_k_value(initial_k = 10, k_rounds = 10)
	print(analizer.get_k())
	analizer.set_stats_for_best_k_value()
	waiting_time_mean_interval = analizer.confidence_interval_for_waiting_time_mean()
	waiting_time_variance_interval = analizer.confidence_interval_for_waiting_time_variance()
	print(waiting_time_mean_interval)
	print(waiting_time_variance_interval)
	center1 = (waiting_time_mean_interval[0] + waiting_time_mean_interval[1])/2
	center2 = (waiting_time_variance_interval[0] + waiting_time_variance_interval[1])/2

	while(not(center1 > waiting_time_variance_interval[1] and center1 < waiting_time_variance_interval[0] and center2 > waiting_time_mean_interval[1] and center2 < waiting_time_mean_interval[1])):
		analizer.set_k(analizer.get_k() + 1000)
		analizer.set_stats_for_best_k_value()
		waiting_time_mean_interval = analizer.confidence_interval_for_waiting_time_mean()
		waiting_time_variance_interval = analizer.confidence_interval_for_waiting_time_variance()
		print(waiting_time_mean_interval)
		print(waiting_time_variance_interval)
		center1 = (waiting_time_mean_interval[0] + waiting_time_mean_interval[1])/2
		center2 = (waiting_time_variance_interval[0] + waiting_time_variance_interval[1])/2

	print(analizer.confidence_interval_for_area_mean())
	print(analizer.confidence_interval_for_area_variance())

start = time.time()

set_best_k_for_variance()

finish = time.time() - start
print("runtime: " + str(round(finish/60, 2)) + " min")
