from typing import List, Tuple
from collections import defaultdict

class PrefixTreeNode:
    def __init__(self):
        self.children: dict[str, 'PrefixTreeNode'] = {}
        self.is_end_of_word = False

class PrefixTree:
    def __init__(self, vocabulary: List[str]):
        self.root = PrefixTreeNode()
        for word in vocabulary:
            self.insert(word)

    def insert(self, word: str):
        node = self.root
        for char in word:
            node = node.children.setdefault(char, PrefixTreeNode())
        node.is_end_of_word = True

    def search_prefix(self, prefix: str) -> List[str]:
        node = self.root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        results = []
        self._dfs(node, prefix, results)
        return results

    def _dfs(self, node: PrefixTreeNode, prefix: str, results: List[str]):
        if node.is_end_of_word:
            results.append(prefix)
        for char, child_node in node.children.items():
            self._dfs(child_node, prefix + char, results)
