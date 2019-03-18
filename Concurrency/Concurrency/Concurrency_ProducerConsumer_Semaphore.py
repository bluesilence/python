# http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/
import threading
import random
import time

class Producer(threading.Thread):
    id = 0

    def __init__(self, integers, empty_semaphore, fill_semaphore):
        threading.Thread.__init__(self)
        self.name = 'Producer-%d' % Producer.id
        Producer.id += 1
        self.integers = integers
        self.empty_semaphore = empty_semaphore
        self.fill_semaphore = fill_semaphore

    def run(self):
        while True:
            self.empty_semaphore.acquire() # Semaphore Counter - 1
            print('empty_semaphore acquired by %s' % self.name)

            integer = random.randint(0, 256)
            self.integers.append(integer)
            print('%d appended to list by %s' % (integer, self.name))

            print('fill_semaphore released by %s' % self.name)
            self.fill_semaphore.release() # Semaphore Counter + 1
            time.sleep(1)

class Consumer(threading.Thread):
    id = 0

    def __init__(self, integers, empty_semaphore, fill_semaphore):
        threading.Thread.__init__(self)
        self.name = 'Consumer-%d' % Consumer.id
        Consumer.id += 1
        self.integers = integers
        self.empty_semaphore = empty_semaphore
        self.fill_semaphore = fill_semaphore

    def run(self):
        while True:
            self.fill_semaphore.acquire() # Semaphore Counter - 1
            print('fill_semaphore acquired by %s' % self.name)

            integer = self.integers.pop()
            print('%d popped from list by %s' % (integer, self.name))

            print('empty_semaphore released by %s' % self.name)
            self.empty_semaphore.release()


def main():
    integers = []
    N = 10
    empty_semaphore = threading.Semaphore(N)
    fill_semaphore = threading.Semaphore(0)

    t1 = Producer(integers, empty_semaphore, fill_semaphore)
    t2 = Consumer(integers, empty_semaphore, fill_semaphore)
    t3 = Consumer(integers, empty_semaphore, fill_semaphore)

    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

if __name__ == '__main__':
    main()