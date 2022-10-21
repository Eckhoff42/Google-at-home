
from Document import Document
from InvertedIndex import InvertedIndex
from Normalizer import Normalizer


class SearchEngine():

    def __init__(self, invertedIndex: InvertedIndex) -> None:
        self.invertedIndex = invertedIndex

    def search_implicit_or(self, query: str) -> list[int]:
        """
        Returns a list of document IDs that matches the query.
        """

        match_list = []
        for term in query.split():
            term = Normalizer.normalize_term(self, term)
            if term in self.invertedIndex.index.keys():
                if len(match_list) == 0:
                    match_list = self.invertedIndex[term]

                else:
                    match_list = self.invertedIndex.merge_terms(
                        match_list, self.invertedIndex[term])

        return match_list

    def get_doc_names(self, doc_ids: list[int], doc_list: list[Document]) -> list[str]:
        """
        Returns a list of document names that matches the document IDs.
        """
        doc_names = []
        for doc_id in doc_ids:
            doc_names.append(doc_list[doc_id].fileName)

        return doc_names
