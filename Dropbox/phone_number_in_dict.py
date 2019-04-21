import collections

class TrieNode:
    def __init__(self):
        self.isLeaf = False
        self.children = collections.defaultdict(TrieNode)
        
    def addWord(self, word):
        node = self
        for ch in word:
            node = node.children[ch]
            
        node.isLeaf = True
        
        
class Solution:
    def letterCombinations(self, digits, dictionary):
        if not digits or '0' in digits or '1' in digits:
            return []
        
        trieRoot = TrieNode()
        for word in dictionary:
            trieRoot.addWord(word)
            
        results = []
        N = len(digits)
        
        mappings = { '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6':'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz' }
        
        def dfs(digits, trieNode, index, result, prefix):
            if index == N:
                if sum(len(word) for word in result) == N:
                    results.append(''.join(result))
                    
                return
            
            digit = digits[index]
            
            for ch in mappings[digit]:
                if ch not in trieNode.children:
                    continue # No matching word in dict

                newPrefix = prefix + ch
                
                if trieNode.children[ch].isLeaf: # Matched a word
                    # Reset trieNode to root
                    # Reset word prefix to ''
                    dfs(digits, trieRoot, index + 1, result + [ newPrefix ], '')
                # Continue searching in Trie tree
                dfs(digits, trieNode.children[ch], index + 1, result, newPrefix)
                
        dfs(digits, trieRoot, 0, [], '')
        
        return results 
    
s = Solution()
digits = "228"
dictionary = [ "cat", "bat", "dev" ]
print(s.letterCombinations(digits, dictionary))
