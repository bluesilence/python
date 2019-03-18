# http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/
import threading
import requests

class FetchUrls(threading.Thread):
    def __init__(self, urls, output, lock):
        threading.Thread.__init__(self)
        self.urls = urls
        self.output = output
        self.lock = lock

    def run(self):
        while self.urls:
            url = self.urls.pop()
            doc = requests.get(url=url)

            with self.lock:
                print('Lock is acquired by %s' % self.name)
                self.output.write(doc.text)
                print('Write is done by %s' % self.name)
                print('Lock is released by %s' % self.name)

            print('URL %s fetched by %s' % (url, self.name))

def main():
    urls1 = [ 'https://stackoverflow.com', 'http://www.facebook.com' ]
    urls2 = [ 'http://www.yahoo.com', 'http://www.youtube.com' ]
    lock = threading.Lock()
    with open('output.txt', 'w+', encoding='utf-8') as f:
        t1 = FetchUrls(urls1, f, lock)
        t2 = FetchUrls(urls2, f, lock)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

if __name__ == '__main__':
    main()