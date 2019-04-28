import collections

class TrieNode:
    def __init__(self):
        self.firstWords = []
        self.children = collections.defaultdict(TrieNode)

class AutoComplete(object):
    """description of class"""
    def __init__(self, topN):
        self.topN = topN
        self.root = TrieNode()

    def add(self, index, word):
        node = self.root
        for ch in word:
            node = node.children[ch]
            if len(node.firstWords) < self.topN:
                node.firstWords.append((index, word))

    def serialize(self):
        results = []

        def dfs(node, prefix):
            if node.firstWords:
                results.append('{}: {}\n'.format(prefix, node.firstWords))

            for ch in sorted(node.children.keys()):
                dfs(node.children[ch], prefix + ch)

        dfs(self.root, '')

        return ''.join(results)

if __name__ == '__main__':
    input_file = './test_autocomplete.txt'
    output_file = './test_autocomplete_output.txt'
    topN = 4

    with open(input_file, 'r') as f:
        index = 0
        lines = f.readlines()
        ac = AutoComplete(topN)
        for line in lines:
            ac.add(index, line.rstrip('\n'))
            index += 1

        with open(output_file, 'w') as f:
            f.write(ac.serialize())
