class Iterator(object):
    def __init__(self, start, stop):
        self.stop = stop
        self.count = start

    def __iter__(self):
        return self

    def next(self):
        if self.count > self.stop:
            raise StopIteration

        count = self.count
        self.count += 1

        return count

import os

class Directory(object):
    def __init__(self, directory):
        self.directory = directory
        self.files = []
        self.dirs = []

        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path):
                self.files.append(entry)
            elif os.path.isdir(full_path):
                self.dirs.append(Directory(full_path))

    def __iter__(self):
        for entry in self.files:
            yield os.path.join(self.directory, entry)

        for directory in self.dirs:
            for entry in directory:
                yield entry