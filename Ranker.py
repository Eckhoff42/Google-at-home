import math

from Document import Document
from CountedInvertedIndex import CountedInvertedIndex


class Ranker():
    def __init__(self, counted_inverted_index: CountedInvertedIndex):
        self.counted_inverted_index = counted_inverted_index

    def calculate_log_frequency(self, frequency: int) -> float:
        """
        Calculate the log frequency of a term in a document
        """
        if (frequency == 0):
            return 0
        else:
            return math.log(frequency, 10) + 1

    def rank_document_query(self, documentId: int, query: list[str]) -> float:
        """
        Rank a document based on a query
        The ranking is based on term frequency weighted by the inverse document frequency
        """
        score = 0
        for term in query:
            tf = self.counted_inverted_index.get_tf(documentId, term)
            idf = self.counted_inverted_index.get_idf(term)
            score += math.log(1 + tf, 10) * idf
        return score

    def rank_documents_query(self, documents: list[int], query: list[str]) -> list[Document]:
        """
        Rank all documents based on a query
        """
        ranked_documents = []
        for documentId in documents:
            ranked_documents.append(
                [documentId, self.rank_document_query(documentId, query)])

        ranked_documents.sort(key=lambda x: x[1], reverse=True)
        return ranked_documents
