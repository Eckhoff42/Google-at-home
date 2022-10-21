from pydoc import plain
from Document import Document


class InvertedIndex():
    def __init__(self):
        # term -> [docID]
        self.index = {}

    def __getitem__(self, term: str):
        if term in self.index:
            return self.index[term]
        else:
            return []

    def __setitem__(self, term: str, docID: int):
        """
        Add a document to the index for a term.
        Duplicate doc_id's are not counted.
        """
        if term in self.index and self.index[term][-1] != docID:
            self.index[term].append(docID)
        else:
            self.index[term] = [docID]

    def __len__(self):
        return len(self.index)

    def __str__(self):
        return str(self.index)

    def build_index(self, docID: int, tokens: list[str]):
        for term in tokens:
            self[term] = docID

    def build_index_from_doc(self, document: Document):
        for term in document.get_tokens():
            self[term] = document.doc_id

    def merge_terms(self, term_a: list[int], term_b: list[int]) -> list[int]:
        """
        Merge two terms into one.
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
                merged.append(term_a[current_a])
                current_a += 1
            else:
                merged.append(term_b[current_b])
                current_b += 1
