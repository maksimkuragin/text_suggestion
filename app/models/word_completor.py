from typing import List, Tuple
from collections import defaultdict
from .prefix_tree import PrefixTree

class WordCompletor:
    def __init__(self, corpus: List[str]):
        self.word_counts = defaultdict(int)
        self.total_words = 0
        for word in corpus:
            self.word_counts[word] += 1
            self.total_words += 1
        self.vocabulary = list(self.word_counts.keys())
        self.prefix_tree = PrefixTree(self.vocabulary)

    def get_words_and_probs(self, prefix: str) -> Tuple[List[str], List[float]]:
        words = self.prefix_tree.search_prefix(prefix)
        probs = [self.word_counts[word] / self.total_words for word in words]
        return words, probs
