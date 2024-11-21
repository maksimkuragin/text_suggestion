from collections import Counter
from typing import List, Tuple

class NGramLanguageModel:
    def __init__(self, corpus: List[List[str]], n: int):
        self.n = n
        self.ngram_counts = Counter()
        self.context_counts = Counter()

        for sentence in corpus:
            length = len(sentence)
            for i in range(length):
                for k in range(1, length - i + 1):
                    ngram = tuple(sentence[i:i+k])
                    self.ngram_counts[ngram] += 1
                    if len(ngram) > 1:
                        context = ngram[:-1]
                        self.context_counts[context] += 1

    def get_next_words_and_probs(self, prefix: List[str]) -> Tuple[List[str], List[float]]:
        """
        Возвращает список слов, которые могут идти после prefix,
        а так же список вероятностей этих слов
        """

        prefix = tuple(prefix)
        total_count = self.context_counts.get(prefix, 0)
        if total_count == 0:
            return [], []

        candidates = {}
        for ngram in self.ngram_counts:
            if len(ngram) == len(prefix) + 1 and ngram[:-1] == prefix:
                next_word = ngram[-1]
                candidates[next_word] = self.ngram_counts[ngram]

        next_words = []
        probs = []
        for word, count in candidates.items():
            prob = count / total_count
            next_words.append(word)
            probs.append(prob)

        return next_words, probs

