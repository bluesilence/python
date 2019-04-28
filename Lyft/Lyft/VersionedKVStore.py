import collections
# https://pypi.org/project/bintrees/
from bintrees import AVLTree

import unittest

class KVStore:
    def __init__(self):
        self.hashmap = collections.defaultdict(AVLTree)

    def set(self, k, value):
        tree = self.hashmap[k]
        new_version = len(tree)

        # Set in a balanced BST: O(logN)
        tree[new_version] = value

    def get(self, k):
        if k not in self.hashmap:
            raise KeyError('Key {} not found.'.format(k))

        tree = self.hashmap[k]
        last_version = len(tree) - 1

        return tree[last_version]

    def getValueWithVersion(self, k, version):
        if k not in self.hashmap:
            raise KeyError('Key {} not found.'.format(k))

        tree = self.hashmap[k]
        last_version = len(tree) - 1

        if version > last_version:
            raise ValueError('Last version {} is smaller than given version {}'.format(last_version, version))

        # Get item in a balanced BST: O(logN)
        return tree[version]

class TestKVStore(unittest.TestCase):
    def test_store(self):
        kvStore = KVStore()
        kvStore.set('a', 1)
        self.assertEqual(kvStore.get('a'), 1)
        kvStore.set('a', 2)
        self.assertEqual(kvStore.get('a'), 2)
        self.assertEqual(kvStore.getValueWithVersion('a', 0), 1)

        kvStore.set('b', 3)
        self.assertRaises(ValueError, kvStore.getValueWithVersion, 'b', 1)

        kvStore.set('c', 4)
        self.assertEqual(kvStore.get('c'), 4)

        self.assertRaises(KeyError, kvStore.get, 'd')
        self.assertRaises(KeyError, kvStore.getValueWithVersion, 'd', 1)

if __name__ == '__main__':
    unittest.main()