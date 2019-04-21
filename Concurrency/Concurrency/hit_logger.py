import random
import time
import threading
from multiprocessing.dummy import Pool
import unittest
from unittest import mock

class HitLogger(object):
    """description of class"""
    def __init__(self, max_size_seconds):
        if max_size_seconds < 1:
            raise ValueError('max_size_seconds should be >= 1')

        self.size = max_size_seconds
        self.counts = [ 0 ] * self.size
        self.times = [ 0 ] * self.size
        self.read_lock = threading.Lock()
        self.write_locks = [ threading.Lock() for _ in range(self.size) ]

    def log_hit(self):
        timestamp = int(time.time())

        print('log hit at ts: {}\n'.format(timestamp))

        time_index = timestamp % self.size

        with self.write_locks[time_index]:
            if self.times[time_index] != timestamp:
                self.counts[time_index] = 0
                self.times[time_index] = timestamp

            self.counts[time_index] += 1

    def get_hits(self):
        timestamp = int(time.time())

        result = 0
        with self.read_lock:
            for ts, count in zip(self.times, self.counts):
                if timestamp >= ts and timestamp - ts < self.size:
                    result += count

        print('get hits at ts: {}, result={}\n'.format(timestamp, result))

        return result

class Test(unittest.TestCase):
#    def test(self):
#        logger = HitLogger(300)
#
#        time.time = mock.Mock(return_value=0)
#        logger.log_hit()
#        time.time = mock.Mock(return_value=10)
#        self.assertEqual(logger.get_hits(), 1)
#        logger.log_hit()
#        self.assertEqual(logger.get_hits(), 2)
#        logger.log_hit()
#        self.assertEqual(logger.get_hits(), 3)
#        time.time = mock.Mock(return_value=100)
#        logger.log_hit()
#        time.time = mock.Mock(return_value=200)
#        logger.log_hit()
#        self.assertEqual(logger.get_hits(), 5)
#        time.time = mock.Mock(return_value=300)
#        logger.log_hit()
#        self.assertEqual(logger.get_hits(), 5)
#        time.time = mock.Mock(return_value=310)
#        self.assertEqual(logger.get_hits(), 3)

    def test_multithread(self):
        logger = HitLogger(300)

        def single_thread_process(logger):
            time.time = mock.Mock(return_value=0)
            logger.log_hit()
            time.sleep(1)
            time.time = mock.Mock(return_value=10)
            logger.get_hits()
            logger.log_hit()
            logger.get_hits()
            logger.log_hit()
            time.sleep(1)
            time.time = mock.Mock(return_value=11)
            logger.get_hits()
            time.sleep(1)
            time.time = mock.Mock(return_value=100)
            logger.log_hit()
            time.sleep(1)
            time.time = mock.Mock(return_value=200)
            logger.log_hit()
            logger.get_hits()
            time.sleep(1)
            time.time = mock.Mock(return_value=300)
            logger.log_hit()
            logger.get_hits()
            time.sleep(1)
            time.time = mock.Mock(return_value=310)
            logger.get_hits()

        pool = Pool(5)
        pool.map(single_thread_process, [ logger ] * 5)

        input('Press any key to exit...')

if __name__ == '__main__':
    unittest.main()

