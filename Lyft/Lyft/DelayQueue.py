from datetime import datetime, timedelta
import heapq
import queue
import random
import threading
import time
import unittest

class Task:
    ID = 0

    def __init__(self, plan_time, src, dst):
        self.plan_time = plan_time
        self.src = src
        self.dst = dst
        self.id = Task.ID
        Task.ID += 1

    def __lt__(self, other):
        return self.plan_time < other.plan_time

    def __str__(self):
        return 'Task {0}: From {1} to {2} at {3}'.format(self.id, self.src, self.dst, self.plan_time)

class DelayQueue(threading.Thread):
    INITIAL_DATETIME = datetime(1970, 1, 1)
    ID = 0

    def __init__(self, tasks_queue, capacity, dispatch_queue):
        threading.Thread.__init__(self)
        self.name = 'DelayQueue-{0}'.format(DelayQueue.ID)
        DelayQueue.ID += 1

        self.tasks_queue = tasks_queue
        self.pq = []
        self.capacity = capacity
        self.dispatch_queue = dispatch_queue

        for i in range(self.capacity):
            if not self.put():
                break

    def put(self):
        if len(self.pq) >= self.capacity:
            return False

        try:
            task = self.tasks_queue.get(timeout=1)
            heapq.heappush(self.pq, task)
            self.tasks_queue.task_done()
            print('{0} has put task {1}\n'.format(self.name, str(task)))

            return True
        except queue.Empty:
            pass

        return False

    def run(self):
        while self.pq or self.tasks_queue.unfinished_tasks > 0:
            # Try to add a new task from incoming queue
            self.put()

            if self.pq:
                task = self.pq[0]
                delta = (task.plan_time - datetime.now()).total_seconds()
                while delta > 0:
                    print('{0}: Task {1} not due yet, wait for {2} seconds...\n'.format(self.name, task.id, delta - 1))
                    time.sleep(delta)

                    task = self.pq[0]
                    delta = (task.plan_time - datetime.now()).total_seconds()

                task = heapq.heappop(self.pq)
                print('{0}: Task {1} is due at {2}, put into dispatch queue...\n'.format(self.name, task.id, task.plan_time))
                self.dispatch_queue.put(task)


class TestDelayQueue(unittest.TestCase):
    def test_scheduling(self):
        dispatch_queue = queue.Queue()
        capacity = 2
        timeout = 30

        start_datetime = datetime.now()
        src_dsts = [ ('Home', 'Office'),
                     ('Safeway', 'Starbucks'),
                     ('Restaurant', 'Mountain'),
                     ('Airport', 'Grocery'),
                     ('HomeDepot', 'Seattle'),
                     ('Beijing', 'Tianjin')
                   ]

        tasks = [ Task(start_datetime + timedelta(seconds=random.randint(1, timeout - 1)), src_dst[0], src_dst[1]) for src_dst in src_dsts ]
        ordered_tasks = sorted(tasks, key=lambda task: task.plan_time)

        task_queue = queue.Queue()
        for task in tasks:
            task_queue.put(task)

        dqs = [ DelayQueue(task_queue, capacity, dispatch_queue) for _ in range(2) ]

        for dq in dqs:
            dq.start()

        for dq in dqs:
            dq.join()

        expected_order = [ task.id for task in ordered_tasks ]
        actual_order = [ task.id for task in dispatch_queue.queue ]
        print('Expected order: {0}'.format(expected_order))
        print('Actual order: {0}'.format(actual_order))

        self.assertEqual(expected_order, actual_order)

if __name__ == '__main__':
    unittest.main() 