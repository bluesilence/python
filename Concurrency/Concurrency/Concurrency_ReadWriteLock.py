# https://gist.github.com/tylerneylon/a7ff6017b7a1f9a506cf75aa23eacfd6
import random
from threading import Lock, Thread
import time
from multiprocessing.dummy import Pool

class Concurrency_ReadWriteLock(object):
    """description of class"""
    def __init__(self):
        self.read_lock = Lock()
        self.write_lock = Lock()
        self.reader_num = 0

    def read_acquire(self):
        with self.read_lock:
            self.reader_num += 1
            print('Reader num: {}'.format(self.reader_num))

            if self.reader_num == 1:
                print('Read is blocking write...')
                self.write_lock.acquire()

    def read_release(self):
        with self.read_lock:
            self.reader_num -= 1
            print('Reader num: {}'.format(self.reader_num))

            if self.reader_num == 0:
                print('No more read, can write now...')
                self.write_lock.release()

    def write_acquire(self):
        print('Request to acquire writer lock...')
        self.write_lock.acquire()
        print('Acquired writer lock')

    def write_release(self):
        self.write_lock.release()
        print('Released writer lock')

class Reader(Thread):
    id = 0

    def __init__(self, rw_lock):
        Thread.__init__(self)

        self.rw_lock = rw_lock
        self.name = 'Reader-{}'.format(Reader.id)
        Reader.id += 1

    def run(self):
        while True:
            self.rw_lock.read_acquire()
            print('{0} is reading...'.format(self.name))
            time.sleep(random.randint(1, 2))
            self.rw_lock.read_release()
            time.sleep(random.randint(1, 20))

class Writer(Thread):
    id = 0

    def __init__(self, rw_lock):
        Thread.__init__(self)

        self.rw_lock = rw_lock
        self.name = 'Writer-{}'.format(Writer.id)
        Writer.id += 1

    def run(self):
        while True:
            self.rw_lock.write_acquire()
            print('{0} is writing...'.format(self.name))
            time.sleep(random.randint(1, 2))
            self.rw_lock.write_release()
            time.sleep(random.randint(1, 5))

if __name__ == '__main__':
    rw_lock = Concurrency_ReadWriteLock()

    reader_count = 5
    writer_count = 3
    readers = []
    writers = []

    for _ in range(reader_count):
        readers.append(Reader(rw_lock))

    for _ in range(writer_count):
        writers.append(Writer(rw_lock))

    for thread in readers + writers:
        thread.start()

    for thread in readers + writers:
        thread.join()
