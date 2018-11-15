from unittest import TestCase

from Scheduler import Scheduler


class TestScheduler(TestCase):

    def test_populate_schedule(self):
        size = 10
        counter = 1

        scheduler = Scheduler(0.6)
        event_list = []
        next_event = scheduler.get_next_event()
        while next_event is not None:
            event_list.append(next_event)
            if next_event[0] == 'a':
                next_event[1].set_departure_time(next_event[1].get_arrival_time() + next_event[1].get_service_time())
                scheduler.schedule_departure(next_event[1])
                if counter < size:
                    scheduler.schedule_next_arrival()
                    counter += 1
            next_event = scheduler.get_next_event()
        self.assertTrue(size*2 == len(event_list))
        for i in range(0, size*2):
            print(f"Event: {event_list[i][0]}\n{event_list[i][1]}")
