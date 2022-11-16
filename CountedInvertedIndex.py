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

    def __str__(self):
        print(self.term_frequency)
        print()
        print(self.document_frequency)
        print()
        return str(self.index)

    def save_document_names(self, filename: str, active_documents: list[Document]):
        """
        Save the document names to a file
        """
        with open(filename, 'w') as file:
            for document in active_documents:
                file.write(str(document.doc_id) + ": " +
                           document.fileName + "\n")

    def read_document_names(self, filename: str):
        """Read the document names from a file"""
        active_documents = []
        with open(filename, 'r') as file:
            for line in file:
                line = line.split(": ")
                document = int(line[0])
                name = line[1]
                active_documents.append(Document(document, name))

        return active_documents

    def write_index_to_file(self, filename: str):
        """
        Write the index to a file
        """
        with open(filename, 'w') as file:
            for term in self.index:
                file.write(term + ": ")
                for doc in self.index[term]:
                    file.write(str(doc[0]) + " " + str(doc[1]) + " ")
                file.write("\n")

    def read_index_from_file(self, filename: str):
        """
        Read the index from a file
        """
        copy = {}
        with open(filename, 'r') as file:
            for line in file:
                line = line.split(": ")
                term = line[0]
                copy[term] = []
                postings = line[1].split(" ")
                for i in range(0, len(postings) - 1, 2):
                    copy[term].append(
                        [int(postings[i]), int(postings[i + 1])])

        self.index = copy
        return copy

    def write_term_frequency_to_file(self, filename: str):
        """
        Write the term frequency to a file
        """
        with open(filename, 'w') as file:
            for document in self.term_frequency:
                file.write(str(document) + ": ")
                for term in self.term_frequency[document]:
                    file.write(
                        term + " " + str(self.term_frequency[document][term]) + " ")
                file.write("\n")

    def read_term_frequency_from_file(self, filename: str):
        """
        Read the term frequency from a file
        """
        copy = {}
        with open(filename, 'r') as file:
            for line in file:
                line = line.split(": ")
                document = int(line[0])
                copy[document] = {}
                terms = line[1].split(" ")
                for i in range(0, len(terms) - 1, 2):
                    copy[document][terms[i]] = int(terms[i + 1])

        self.term_frequency = copy
        return copy

    def write_document_frequency_to_file(self, filename: str):
        """
        Write the document frequency to a file
        """
        with open(filename, 'w') as file:
            for term in self.document_frequency:
                file.write(term + ": " +
                           str(self.document_frequency[term]) + "\n")

    def read_document_frequency_from_file(self, filename: str):
        """
        Read the document frequency from a file
        """
        copy = {}
        with open(filename, 'r') as file:
            for line in file:
                line = line.split(": ")
                term = line[0]
                copy[term] = int(line[1])

        self.document_frequency = copy
        return copy

    def save(self, filename: str):
        """Save the index to a file"""
        self.write_index_to_file(filename + ".index")
        self.write_term_frequency_to_file(filename + ".tf")
        self.write_document_frequency_to_file(filename + ".df")

    def read(self, filename: str):
        """Read the index from a file"""
        self.read_index_from_file(filename + ".index")
        self.read_term_frequency_from_file(filename + ".tf")
        self.read_document_frequency_from_file(filename + ".df")

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
