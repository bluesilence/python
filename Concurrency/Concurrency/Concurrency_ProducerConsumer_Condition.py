# http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/
import threading
import random
import time

class Producer(threading.Thread):
    id = 0

    def __init__(self, integers, condition):
        threading.Thread.__init__(self)
        self.name = 'Producer-%d' % Producer.id
        Producer.id += 1
        self.integers = integers
        self.condition = condition

    def run(self):
        while True:
            integer = random.randint(0, 256)
            self.condition.acquire()
            print('condition acquired by %s' % self.name)
            self.integers.append(integer)
            print('%d appended to list by %s' % (integer, self.name))
            print('condition notified by %s' % self.name)
            self.condition.notify()
            print('condition released by %s' % self.name)
            self.condition.release()
            time.sleep(1)

class Consumer(threading.Thread):
    id = 0

    def __init__(self, integers, condition):
        threading.Thread.__init__(self)
        self.name = 'Consumer-%d' % Consumer.id
        Consumer.id += 1
        self.integers = integers
        self.condition = condition

    def run(self):
        while True:
            self.condition.acquire()
            print('condition acquired by %s' % self.name)
            while True:
                if self.integers:
                    integer = self.integers.pop()
                    print('%d popped from list by %s' % (integer, self.name))
                    break

                print('condition waited by %s' % self.name)
                self.condition.wait()

            print('condition released by %s' % self.name)
            self.condition.release()


def main():
    integers = []
    condition = threading.Condition()
    t1 = Producer(integers, condition)
    t2 = Consumer(integers, condition)
    t3 = Consumer(integers, condition)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

if __name__ == '__main__':
    main()