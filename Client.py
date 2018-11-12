class Client:

    def __init__(self, arrival_time, service_time):
        self.__arrival_time = arrival_time
        self.__service_time = service_time

    def get_arrival_time(self):
        return self.__arrival_time

    def get_service_time(self):
        return self.__service_time
