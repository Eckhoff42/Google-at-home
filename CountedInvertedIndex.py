import math
import PersistentStorage
from pydoc import plain
from Document import Document
from BaseInvertedIndex import BaseInvertedIndex


class CountedInvertedIndex(BaseInvertedIndex):
    def __init__(self):
        # term -> [[docID, count]]
        self.index = {}
        self.term_frequency = {}
        self.document_frequency = {}

    def __str__(self):
        print(self.term_frequency)
        print()
        print(self.document_frequency)
        print()
        return str(self.index)

    def save(self):
        """Save the index to a file"""
        PersistentStorage.write_index_to_file(
            self.index, "save/index.txt")
        PersistentStorage.write_term_frequency_to_file(
            self.term_frequency, "save/tf.txt")
        PersistentStorage.write_document_frequency_to_file(
            self.document_frequency, "save/df.txt")

    def load(self):
        """Read the index from a file"""
        self.index = PersistentStorage.read_index_from_file(
            "save/index.txt")
        self.term_frequency = PersistentStorage.read_term_frequency_from_file(
            "save/tf.txt")
        self.document_frequency = PersistentStorage.read_document_frequency_from_file(
            "save/df.txt")

    def get_doc_ids(self) -> list[int]:
        """Get the document IDs in the collection"""
        return list(self.term_frequency.keys())

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
        for posting in self.index.values():
            total_terms += len(posting)

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

    def print_stats(self):
        """Print the index statistics"""
        print("Number of documents: ", len(self.term_frequency))
        print("Number of terms: ", len(self.index))
        print("Number of postings: ", self._total_terms())
