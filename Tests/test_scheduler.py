from unittest import TestCase

from Scheduler import Scheduler


class TestScheduler(TestCase):

    def setUp(self):
        """Initializes the Scheduler"""
        self.__scheduler = Scheduler()

    def test_build_and_get_queue(self):
        """Builds a queue with size 'size' and retrieves it,
        checking if the arrival times are cumulative"""
        start = 0
        test = True
        last_arrival = start
        size = 10000

        self.__scheduler.build_queue(size, start)
        res = self.__scheduler.get_queue()
        for i in range(0, size):
            arrival = res[i].get_arrival_time()
            if arrival < last_arrival:
                test = False
            # print(f"Arrival time: {arrival}\n"
            #       f"service time: {res[i].get_service_time()}\n")
        self.assertTrue(test)
