# http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/
import threading
import random
import time
import queue

class Producer(threading.Thread):
    id = 0

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.name = 'Producer-%d' % Producer.id
        Producer.id += 1
        self.queue = queue

    def run(self):
        while True:
            integer = random.randint(0, 256)
            self.queue.put(integer)
            print('%d appended to list by %s' % (integer, self.name))
            time.sleep(1)

class Consumer(threading.Thread):
    id = 0

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.name = 'Consumer-%d' % Consumer.id
        Consumer.id += 1
        self.queue = queue

    def run(self):
        while True:
            integer = self.queue.get()
            print('%d popped from list by %s' % (integer, self.name))
            self.queue.task_done()

def main():
    q = queue.Queue()
    num_producers = 2
    num_consumers = 3

    producers = []
    for _ in range(num_producers):
        p = Producer(q)
        p.start()
        producers.append(p)

    consumers = []
    for _ in range(num_consumers):
        c = Consumer(q)
        c.start()
        consumers.append(c)

    for t in producers + consumers:
        t.join()

if __name__ == '__main__':
    main()