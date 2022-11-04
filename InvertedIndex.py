from pydoc import plain
from Document import Document
from BaseInvertedIndex import BaseInvertedIndex


class InvertedIndex(BaseInvertedIndex):
    def __init__(self):
        # term -> [docID]
        self.index = {}

    def build_index(self, docID: int, tokens: list[str]):
        for term in tokens:
            self[term] = docID

    def build_index_from_doc(self, document: Document):
        for term in document.get_tokens():
            self[term] = document.doc_id

    def merge_or(self, term_a: list[int], term_b: list[int]) -> list[int]:
        """
        Merge two posting lists into one
        """
        current_a = 0
        current_b = 0

        merged = []
        while current_a < len(term_a) and current_b < len(term_b):
            if term_a[current_a] == term_b[current_b]:
                merged.append(term_a[current_a])
                current_a += 1
                current_b += 1
            elif term_a[current_a] < term_b[current_b]:
                merged.append(term_a[current_a])
                current_a += 1
            else:
                merged.append(term_b[current_b])
                current_b += 1

        if current_a < len(term_a):
            merged.extend(term_a[current_a:])
        elif current_b < len(term_b):
            merged.extend(term_b[current_b:])
        return merged

    def merge_and(self, term_a: list[int], term_b: list[int]) -> list[int]:
        """
        Merge two posting lists into one where IDs are equal
        """
        current_a = 0
        current_b = 0

        merged = []
        while current_a < len(term_a) and current_b < len(term_b):
            print(term_a[current_a], term_b[current_b])
            if term_a[current_a] == term_b[current_b]:
                merged.append(term_a[current_a])
                current_a += 1
                current_b += 1
            elif term_a[current_a] < term_b[current_b]:
                current_a += 1
            else:
                current_b += 1
        return merged
