# http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/
import threading
import random
import time

class Producer(threading.Thread):
    id = 0

    def __init__(self, integers, event):
        threading.Thread.__init__(self)
        self.name = 'Producer-%d' % Producer.id
        Producer.id += 1
        self.integers = integers
        self.event = event

    def run(self):
        while True:
            integer = random.randint(0, 256)
            self.integers.append(integer)
            print('%d appended to list by %s' % (integer, self.name))

            print('event set by %s' % self.name)
            self.event.set()
            self.event.clear()
            print('event cleared by %s' % self.name)
            time.sleep(1)

class Consumer(threading.Thread):
    id = 0

    def __init__(self, integers, event):
        threading.Thread.__init__(self)
        self.name = 'Consumer-%d' % Consumer.id
        Consumer.id += 1
        self.integers = integers
        self.event = event

    def run(self):
        while True:
            self.event.wait()
            try:
                integer = self.integers.pop()
                print('%d popped from list by %s' % (integer, self.name))
            except IndexError:
                # catch pop on empty list
                print('No integer to consume, %s is going to sleep...' % self.name)
                time.sleep(1)

def main():
    integers = []
    N = 10
    event = threading.Event()

    t1 = Producer(integers, event)
    t2 = Consumer(integers, event)
    t3 = Consumer(integers, event)

    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

if __name__ == '__main__':
    main()