import math
from pydoc import plain
from Document import Document
from BaseInvertedIndex import BaseInvertedIndex


class CountedInvertedIndex(BaseInvertedIndex):
    def __init__(self):
        # term -> [[docID, count]]
        self.index = {}
        self.term_frequency = {}
        self.document_frequency = {}

    def build_document_frequency(self):
        for term in self.index:
            self.document_frequency[term] = len(self.index[term])

    def build_index(self, docID: int, tokens: list[str]):
        doc_counted = False
        self.term_frequency[docID] = {}
        for term in tokens:
            # first time we see the term
            if term not in self.index:
                self.index[term] = []
                self.index[term].append([docID, 1])
            elif self.index[term][-1][0] != docID:
                self.index[term].append([docID, 1])
            else:
                self.index[term][-1][1] += 1

            # update term frequency
            if term not in self.term_frequency[docID]:
                self.term_frequency[docID][term] = 1
            else:
                self.term_frequency[docID][term] += 1

        self.build_document_frequency()

    # def get_term_frequency(self) -> int:
    #     return self.term_frequency

    # def get_document_frequency(self) -> int:
    #     return self.document_frequency

    def merge_and(self, term_a: list[list[int, int]], term_b: list[list[int, int]]) -> list[list[int, int]]:
        """
        Merge two posting lists into one where IDs are equal
        """
        current_a = 0
        current_b = 0

        merged = []
        while current_a < len(term_a) and current_b < len(term_b):
            if term_a[current_a][0] == term_b[current_b][0]:
                merged.append(
                    [term_a[current_a][0], term_a[current_a][1] + term_b[current_b][1]])
                current_a += 1
                current_b += 1
            elif term_a[current_a][0] < term_b[current_b][0]:
                current_a += 1
            else:
                current_b += 1
        return merged

    def merge_or(self, term_a: list[list[int, int]], term_b: list[list[int, int]]) -> list[list[int, int]]:
        """
        Merge two posting lists into one
        """
        current_a = 0
        current_b = 0

        merged = []
        while current_a < len(term_a) and current_b < len(term_b):
            if term_a[current_a][0] == term_b[current_b][0]:
                merged.append(
                    [term_a[current_a][0], term_a[current_a][1] + term_b[current_b][1]])
                current_a += 1
                current_b += 1
            elif term_a[current_a][0] < term_b[current_b][0]:
                merged.append(
                    [term_a[current_a][0], term_a[current_a][1] + term_b[current_b][1]])
                current_a += 1
            else:
                merged.append(
                    [term_b[current_b][0], term_b[current_b][1] + term_a[current_a][1]])
                current_b += 1

        if current_a < len(term_a):
            merged.extend(term_a[current_a:])
        elif current_b < len(term_b):
            merged.extend(term_b[current_b:])

        return merged

    def _total_terms(self) -> int:
        """Get the total number of terms in the collection"""
        total_terms = 0
        for document in self.document_frequency:
            for term in self.document_frequency[document]:
                total_terms += self.document_frequency[document][term]

        return total_terms

    def get_tf(self, document_id: int, term: str) -> int:
        """Get the term frequency of a term"""
        if term in self.term_frequency[document_id]:
            return self.term_frequency[document_id][term]
        else:
            return 0

    def get_df(self, term: str) -> int:
        """Get the document frequency of a term"""
        if term in self.document_frequency:
            return self.document_frequency[term]
        else:
            return 0

    def get_idf(self, term) -> int:
        """Get the inverse document frequency of a term"""
        if term in self.document_frequency:
            return math.log((len(self.term_frequency) / self.get_df(term)), 10)
        else:
            return 0
