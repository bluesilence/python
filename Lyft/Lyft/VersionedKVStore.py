# https://www.1point3acres.com/bbs/forum.php?mod=viewthread&tid=308308

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

    def unset(self, k):
        if k not in self.hashmap:
            raise KeyError('Key {} not found.'.format(k))

        tree = self.hashmap[k]
        last_version = len(tree) - 1

        # Remove from a balanced BST: O(logN)
        return tree.pop(last_version) # Remove last version

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

    def processLine(self, line):
        tokens = line.upper().split(' ')
        command = tokens[0]
        if command == 'SET':
            assert(len(tokens) == 3)

            self.set(tokens[1], tokens[2])
        elif command == 'UNSET':
            assert(len(tokens) == 2)

            return self.unset(tokens[1])
        elif command == 'GET':
            assert(len(tokens) == 2)

            return self.get(tokens[1])
        elif command == 'GETVERSION':
            assert(len(tokens) == 3)

            return self.getValueWithVersion(tokens[1], int(tokens[2]))
        else:
            raise NotImplementedError('Unsupported command: {}'.format(command))

    def serialize(self):
        result = []
        for key in sorted(self.hashmap.keys()):
            tree = self.hashmap[key]

            if len(tree):
                result.append('Key {}:'.format(key))
                for version in range(len(tree)):
                    result.append('Version {}: {}'.format(version, tree[version]))

        return ' '.join(result)

class TestKVStore(unittest.TestCase):
    def test_store(self):
        kvStore = KVStore()
        kvStore.set('a', 1)
        self.assertEqual(kvStore.get('a'), 1)
        kvStore.set('a', 2)
        self.assertEqual(kvStore.get('a'), 2)
        self.assertEqual(kvStore.getValueWithVersion('a', 0), 1)
        kvStore.unset('a')
        self.assertEqual(kvStore.get('a'), 1)

        kvStore.set('b', 3)
        self.assertRaises(ValueError, kvStore.getValueWithVersion, 'b', 1)

        kvStore.set('c', 4)
        self.assertEqual(kvStore.get('c'), 4)

    def test_lines(self):
        kvStore = KVStore()

        kvStore.processLine('SET a 1')
        self.assertEqual(kvStore.processLine('GET a'), '1')
        kvStore.processLine('SET b 2')
        self.assertEqual(kvStore.processLine('GET b'), '2')
        kvStore.processLine('UNSET b')
        self.assertRaises(KeyError, kvStore.processLine, 'GET b')
        self.assertRaises(ValueError, kvStore.processLine, 'GETVERSION a 1')
        kvStore.processLine('SET a 3')
        self.assertEqual(kvStore.processLine('GET a'), '3')
        self.assertEqual(kvStore.processLine('GETVERSION a 1'), '3')

    def test_serialize(self):
        kvStore = KVStore()
        kvStore.set('a', 1)
        kvStore.set('a', 2)
        kvStore.set('b', 3)
        serialized = kvStore.serialize()

        self.assertEqual(serialized, 'Key a: Version 0: 1 Version 1: 2 Key b: Version 0: 3')

if __name__ == '__main__':
    unittest.main()