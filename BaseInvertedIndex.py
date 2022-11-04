
from abc import abstractmethod


class BaseInvertedIndex():
    def __init__(self):
        self.index = {}

    def __getitem__(self, term: any):
        if term in self.index:
            return self.index[term]
        else:
            return []

    def __setitem__(self, term: str, value: any):
        """
        Add a document to the index for a term.
        Duplicate doc_id's are not counted.
        """
        if term in self.index and self.index[term][-1] != value:
            self.index[term].append(value)
        else:
            self.index[term] = [value]

    def __len__(self):
        return len(self.index)

    def __str__(self):
        return str(self.index)

    @abstractmethod
    def build_index(self, docID: int, tokens: list[str]):
        pass
