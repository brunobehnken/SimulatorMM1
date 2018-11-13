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

        self.__scheduler.build_queue(size, start, 1)
        res = self.__scheduler.get_queue()
        for i in range(0, size):
            arrival = res[i].get_arrival_time()
            if arrival < last_arrival:
                test = False
            # print(f"Arrival time: {arrival}\n"
            #       f"service time: {res[i].get_service_time()}\n")
        self.assertTrue(test)

    def test_start_time(self):
        """Builds queues with start_flag as True and then as False,
        checking if the resulting start times are correct"""
        start = 0
        test = True
        size = 2

        self.__scheduler.build_queue(size, start, 1, True)
        res = self.__scheduler.get_queue()
        if res[0].get_arrival_time() != start:
            test = False
        self.assertTrue(test)

        self.__scheduler.empty_queue()
        self.__scheduler.build_queue(size, start, 1)
        res = self.__scheduler.get_queue()
        if res[0].get_arrival_time() == start:
            test = False
        self.assertTrue(test)

    def test_empty_queue(self):
        """Builds a queue, make it empty, retrieve the queue
        and compares it with the an empty list"""
        start = 20
        size = 10

        self.__scheduler.build_queue(size, start)
        self.__scheduler.empty_queue()
        res = self.__scheduler.get_queue()
        self.assertTrue(res == [])

    def test_queue_size(self):
        """Check if the queue is being created with the intended size"""
        start = 20
        size = 10

        self.__scheduler.build_queue(size, start)
        self.__scheduler.build_queue(size, start)
        self.__scheduler.build_queue(size, start)
        res = self.__scheduler.get_queue()
        self.assertTrue(len(res) == size * 3)
