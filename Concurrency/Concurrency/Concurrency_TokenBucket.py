import threading
import time
import random

class TokenBucket(threading.Thread):
    def __init__(self, max_tokens, interval):
        threading.Thread.__init__(self)

        self.tokens = 0
        self.lock = threading.Lock()
        self.max_tokens = max_tokens
        self.interval = interval

    def run(self):
        while True:
            if self.tokens < self.max_tokens:
                with self.lock:
                    self.tokens += 1
                    print('TokenBucket now has {} tokens...'.format(self.tokens))

            time.sleep(self.interval)

    def get_tokens(self):
        return self.tokens

    def take_tokens(self, tokens_num):
        with self.lock:
            if tokens_num <= self.tokens:
                self.tokens -= tokens_num
                print('TokenBucket removed {} tokens, {} tokens left.'.format(tokens_num, self.tokens))
                return True
            else:
                print('Required {} tokens but only has {}.'.format(tokens_num, self.tokens))

            return False

class Packet(threading.Thread):
    id = 0

    def __init__(self, size, arrive_time, token_bucket):
        threading.Thread.__init__(self)

        self.name = 'Packet-%d' % Packet.id
        Packet.id += 1
        self.size = size
        self.arrive_time = arrive_time
        self.token_bucket = token_bucket

    def run(self):
        time.sleep(self.arrive_time)

        if self.token_bucket.take_tokens(self.size):
            print('{} acquired {} tokens and was passed.'.format(self.name, self.size))
        else:
            print('{} did not get enough tokens and is non-conformant.'.format(self.name))

def main():
    N = 10
    max_tokens = 100
    interval = 1
    bucket = TokenBucket(max_tokens, interval)
    packets = [ Packet(random.randint(1, max_tokens), random.randint(1, max_tokens * 3), bucket) for _ in range(N) ]

    bucket.start()
    for packet in packets:
        packet.start()

    for packet in packets:
        packet.join()

    bucket.join()

if __name__ == '__main__':
    main()
