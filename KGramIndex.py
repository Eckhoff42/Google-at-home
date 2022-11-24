from BaseInvertedIndex import BaseInvertedIndex


class KGramIndex(BaseInvertedIndex):
    def __init__(self, k=2):
        self.k = k
        self.index = {}

    def __str__(self):
        comb = ""
        for kgram in self.index:
            comb += f"{kgram}: {self.index[kgram]}\n"
        return comb

    def get_kgrams(self, term: str) -> list[str]:
        term = "$" + term + "$"
        kgrams = []
        for i in range(len(term) - self.k + 1):
            if term[i+self.k-1] == "*":
                break
            kgrams.append(term[i:i+self.k])
        return kgrams

    def index_term(self, term: str):
        kgrams = self.get_kgrams(term)
        for kgram in kgrams:
            if kgram not in self.index:
                self.index[kgram] = set()
            self.index[kgram].add(term)

    def index_terms(self, terms: list[str]):
        for term in terms:
            self.index_term(term)

    def evaluate(self, wildcardQuery: str) -> list[str]:
        kgrams = self.get_kgrams(wildcardQuery)
        print(kgrams)
        result_postings = []
        for kgram in kgrams:
            if kgram in self.index:
                result_postings.append(self.index[kgram])

        # get the terms that are in all postings
        result = result_postings[0]
        for posting in result_postings:
            result = result.intersection(posting)

        return result
