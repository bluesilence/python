import threading
import time
import random
import heapq

class TokenBucket(threading.Thread):
    def __init__(self, max_tokens, interval):
        threading.Thread.__init__(self)

        self.tokens = 0
        self.lock = threading.Lock()
        self.max_tokens = max_tokens
        self.interval = interval
        self.min_heap = [] # Process packats requesting fewer tokens first

    def run(self):
        while True:
            if self.tokens < self.max_tokens:
                with self.lock:
                    self.tokens += 1
                    print('TokenBucket now has {} tokens...'.format(self.tokens))

            self.process_requests()

            time.sleep(self.interval)

    def process_requests(self):
        with self.lock:
            while self.min_heap and self.min_heap[0].size <= self.tokens:
                packet = heapq.heappop(self.min_heap)
                self.tokens -= packet.size
                print('TokenBucket removed {} tokens for packet {}, {} tokens left.'.format(packet.size, packet.name, self.tokens))
                packet.event.set()

    def add_requests(self, packet, tokens_num):
        with self.lock: # heapq is not thread safe
            heapq.heappush(self.min_heap, packet)
            print('Packet {} requests for {} tokens, current requests: {}'.format(packet.name, tokens_num, [ p.size for p in self.min_heap ] ))

class Packet(threading.Thread):
    id = 0

    def __init__(self, size, arrive_time, token_bucket, event):
        threading.Thread.__init__(self)

        self.name = 'Packet-%d' % Packet.id
        Packet.id += 1
        self.size = size
        self.arrive_time = arrive_time
        self.token_bucket = token_bucket
        self.event = event

    def __lt__(self, other):
        return self.size < other.size or self.size == other.size and self.id < other.id

    def run(self):
        self.event.clear()

        self.token_bucket.add_requests(self, self.size)

        self.event.wait()
        print('{} acquired {} tokens and was passed.'.format(self.name, self.size))

        time.sleep(self.arrive_time)

def main():
    N = 10
    max_tokens = 100
    interval = 1
    bucket = TokenBucket(max_tokens, interval)
    packets = [ Packet(random.randint(1, max_tokens // 10), random.randint(1, max_tokens * 3), bucket, threading.Event()) for _ in range(N) ]

    bucket.start()
    for packet in packets:
        packet.start()

    for packet in packets:
        packet.join()

    bucket.join()

if __name__ == '__main__':
    main()
