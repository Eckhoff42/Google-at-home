
from Compressor import Compressor
from Document import Document
from InvertedIndex import InvertedIndex
from Normalizer import Normalizer


class SearchEngine():

    def __init__(self, invertedIndex: InvertedIndex) -> None:
        self.invertedIndex = invertedIndex

    def search(self, query: str, operator: str = "AND") -> list[int]:
        """
        Returns a list of document IDs that matches the query.
        """

        match_list = []
        for term in query.split():
            term = Normalizer.normalize_term(self, term)
            term = Normalizer.stem_term(self, term)
            if term in self.invertedIndex.index.keys():
                if len(match_list) == 0:
                    match_list = self.invertedIndex[term]

                else:
                    if (operator == "AND"):
                        match_list = self.invertedIndex.merge_and(
                            match_list, self.invertedIndex[term])
                    elif (operator == "OR"):
                        match_list = self.invertedIndex.merge_or(
                            match_list, self.invertedIndex[term])
                    else:
                        # error invalid operator
                        print("Invalid operator")
                        return

        return match_list

    def __next_document(self, posting_lists, cursors):
        smallest = None
        for list_index, internal_index in cursors:
            current_posting_list = posting_lists[list_index]
            if internal_index >= len(current_posting_list):
                continue
            if smallest == None or current_posting_list[internal_index] < smallest:
                smallest = current_posting_list[internal_index]

        return smallest

    def __move_cursors(self, posting_lists, cursors, done_document):
        for cursor_index in range(len(cursors)):
            list_index, internal_index = cursors[cursor_index]
            if posting_lists[list_index][internal_index] == done_document:
                cursors[cursor_index] = (
                    cursors[cursor_index][0], cursors[cursor_index][1] + 1)

    def __count_occurrences(self, posting_lists, cursors, doc_id):
        count = 0
        for cursor_index in range(len(cursors)):
            list_index, internal_index = cursors[cursor_index]
            if posting_lists[list_index][internal_index] == doc_id:
                count += 1

        return count

    def search_n_of_m(self, query: str, match_percentage: int) -> list[int]:
        """
        Returns a list of document IDs where at least `match_percentage`% of the terms are included.
        """

        m = len(query.split())
        n = max(1, min(m, (m * (match_percentage / 100))))
        posting_lists = []
        cursors = []
        match_list = []

        # initialize posting lists and cursors
        for term in query.split():
            term = Normalizer.normalize_term(self, term)
            term = Normalizer.stem_term(self, term)
            if term in self.invertedIndex.index.keys():
                posting_lists.append(self.invertedIndex[term])
                cursors.append((len(posting_lists)-1, 0))

        print(posting_lists)
        print(cursors)

        # document at a time traversal
        current_doc = self.__next_document(posting_lists, cursors)
        while current_doc != None:
            nr_of_hits = self.__count_occurrences(
                posting_lists, cursors, current_doc)

            print(current_doc, " hits ", nr_of_hits, " n is", n)
            if nr_of_hits >= n:
                match_list.append(current_doc)

            self.__move_cursors(posting_lists, cursors, current_doc)
            current_doc = self.__next_document(posting_lists, cursors)

        return match_list

    def get_doc_names(self, doc_ids: list[int], doc_list: list[Document]) -> list[str]:
        """
        Returns a list of document names that matches the document IDs.
        """
        doc_names = []
        for doc_id in doc_ids:
            doc_names.append(doc_list[doc_id].fileName)

        return doc_names
