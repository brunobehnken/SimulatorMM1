from Scheduler import Scheduler


class Simulator:

    def __init__(self):
        self.__currentTime = 0

    def __server(self, client):
        self.__currentTime += client.get_service_time()
        del client

    # noinspection PyPep8Naming
    def run_sample_FCFS(self, size, param_lambda):
        """Runs one sample of the FCFS queue with size 'size'
        and arrival rate 'param_lambda', collecting statistics"""
        queue = []
        scheduler = Scheduler()
        upcoming = scheduler.build_queue(size, 0, param_lambda, True)
        queue.append(upcoming.pop(0))  # first client arrival

        # start of the simulation
        while True:
            self.__server(queue.pop(0))  # next client at the queue served
            while len(upcoming) != 0 and upcoming[0].get_arrival_time() < self.__currentTime:  # updating queue
                queue.append(upcoming.pop(0))
            # gather statistics: size of the queue and wait-time for the next client (???)
            if len(queue) == 0:
                if len(upcoming) == 0:
                    break  # end of the simulation
                else:  # the server is idle
                    queue.append(upcoming.pop(0))
                    self.__currentTime = queue[0].get_arrival_time()
