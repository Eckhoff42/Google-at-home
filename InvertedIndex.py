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
        if term in self.index:
            self.index[term].append(docID)
        else:
            self.index[term] = [docID]

    def __len__(self):
        return len(self.index)

    def __str__(self):
        return str(self.index)
