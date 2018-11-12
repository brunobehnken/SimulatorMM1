class Client:
    """This class was made to represent a client that
    arrives at the queue and is server by the server"""

    def __init__(self, arrival_time, service_time):
        """Sets the arrival time and the service time"""
        self.__arrival_time = arrival_time
        self.__service_time = service_time

    def get_arrival_time(self):
        """Returns the arrival time"""
        return self.__arrival_time

    def get_service_time(self):
        """Returns the service time"""
        return self.__service_time
