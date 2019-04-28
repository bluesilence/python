import unittest

class APICalls(object):
    """description of class"""
    def __init__(self):
        self.apiMap = dict()

    def register(self, signal_id, callable):
        self.apiMap[signal_id] = callable

    def signal(self, signal_id):
        if signal_id not in self.apiMap:
            raise KeyError('Signal {} not registered!'.format(signal_id))

        self.apiMap[signal_id]()

    def remove(self, signal_id):
        if signal_id in self.apiMap:
            self.apiMap.pop(signal_id)

class TestAPICalls(unittest.TestCase):
    def test_normalcases(self):
        call = APICalls()
        call.register(0, lambda: print('Callable 0'))
        call.register(1, lambda: print('Callable 1'))
        call.signal(0)
        call.signal(1)
        call.remove(0)
        self.assertRaises(KeyError, call.signal, 0)

if __name__ == '__main__':
    unittest.main()