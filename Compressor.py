from InvertedIndex import InvertedIndex


class Compressor():
    def __init__(self, stop_list: list[str]) -> None:
        self.stop_list = stop_list

    def compress_inverted_index_stop_words(self, inverted_index: InvertedIndex) -> None:
        """
        Compresses the inverted index by removing stop words.
        These are common words that carry little meaning
        """
        del_terms = []
        for term in inverted_index.index.keys():
            if term in self.stop_list:
                del_terms.append(term)

        for term in del_terms:
            del inverted_index.index[term]
