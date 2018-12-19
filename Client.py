class Client:
    """This class was made to represent a client that
    arrives at the queue and is server by the server"""

    def __init__(self, arrival_time, service_time, round_num):
        """Sets the arrival time, service time and round number of the client"""
        self.__arrival_time = arrival_time
        self.__service_time = service_time
        self.__round_num = round_num
        self.__wait_time = None
        self.__departure_time = None

    def get_arrival_time(self):
        """Returns the arrival time"""
        return self.__arrival_time

    def get_service_time(self):
        """Returns the service time"""
        return self.__service_time

    def get_round(self):
        """Returns the round number of the client"""
        return self.__round_num

    def get_wait_time(self):
        """Returns the wait time"""
        return self.__wait_time

    def set_wait_time(self, wait_time):
        """Sets the wait time if possible"""
        if self.__wait_time is None:
            self.__wait_time = wait_time

    def get_departure_time(self):
        """Returns the departure time"""
        return self.__departure_time

    def set_departure_time(self, departure_time):
        """Sets the departure time if possible"""
        if self.__departure_time is None:
            self.__departure_time = departure_time

    def __str__(self):
        return f"Arrival time: {self.__arrival_time}\n" \
               f"Service time: {self.__service_time}\n" \
               f"Wait time: {self.__wait_time}\n" \
               f"Departure time: {self.__departure_time}\n"
