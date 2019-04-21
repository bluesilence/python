# http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/
import threading
import requests
import queue
import time
import enum

class Status(enum.Enum):
    NEW = 0,
    WORKING = 1,
    PENDING = 2,
    STOPPING = 3,
    STOPPED = 4

class Crawler(threading.Thread):
    def __init__(self, id, queue, processed_set, lock, timeout=1):
        threading.Thread.__init__(self)
        self.name = 'Crawler-{}'.format(id)
        self.queue = queue
        self.processed = processed_set
        self.lock = lock
        self.status = Status.NEW
        self.timeout = timeout

    def parse_urls(self, doc):
        return []

    def run(self):
        while True:
            try:
                url = self.queue.get(timeout=self.timeout)
                self.status = Status.WORKING
                doc = requests.get(url=url, headers={'Accept-Encoding': ''})
                self.queue.task_done()

                print('{} crawled {}'.format(self.name, url))

                with lock:
                    self.processed.add(url)

                new_urls = self.parse_urls(doc)
                for new_url in new_urls:
                    if new_url in self.processed or new_url in self.queue:
                        continue

                    self.queue.put(new_url)
            except queue.Empty:
                if self.status == Status.STOPPING:
                    print('{}: Stopping...'.format(self.name))
                    break # Terminate the thread

                if self.status != Status.PENDING:
                    print('{}: Change status to PENDING...'.format(self.name))
                    self.status = Status.PENDING

                time.sleep(1)

        self.status = Status.STOPPED
        print('{} has stopped.'.format(self.name))

if __name__ == '__main__':
    urls = [ 'https://stackoverflow.com', 'http://www.facebook.com', 'http://www.yahoo.com', 'http://www.youtube.com' ]
    lock = threading.Lock()
    q = queue.Queue()

    for url in urls:
        q.put(url)

    N_threads = 5
    crawlers = []
    processed = set()

    for i in range(N_threads):
        crawler = Crawler(i, q, processed, lock)
        crawlers.append(crawler)

        crawler.start()

    while True:
        if not any(crawler.status == Status.WORKING for crawler in crawlers):
            for crawler in crawlers:
                if crawler.status != Status.STOPPED:
                    crawler.status = Status.STOPPING
                    crawler.join()

            break

        time.sleep(1)
