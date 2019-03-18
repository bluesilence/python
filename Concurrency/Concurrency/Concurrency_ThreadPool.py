# http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/
import threading
import random
import time
import queue

class Worker(threading.Thread):
    id = 0

    def __init__(self, tasks):
        threading.Thread.__init__(self)
        self.name = 'Worker-%d' % Worker.id
        Worker.id += 1

        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                print('%s is working...' % self.name)
                func(*args, **kwargs)
            except Exception as e:
                print(e)
            finally:
                print('%s has done one task.' % self.name)
                self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = queue.Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def map(self, func, args_list):
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        self.tasks.join()
        print('All tasks completed.')

def main():
    def wait_delay(d):
        print('sleep for %d seconds...' % d)
        time.sleep(d)

    delays = [ random.randrange(3, 7) for i in range(50) ]

    pool = ThreadPool(5)
    pool.map(wait_delay, delays)
    pool.wait_completion()

if __name__ == '__main__':
    main()