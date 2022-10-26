
from Compressor import Compressor
from Normalizer import Normalizer
from Document import Document
from InvertedIndex import InvertedIndex
from SearchEngine import SearchEngine


def read_documents(filenames: str) -> list[Document]:
    documents = []
    for i, filename in enumerate(filenames):
        documents.append(Document(i, open(filename).read(), filename))
    return documents


if __name__ == '__main__':
    document_names = ['norge.txt', 'sverige.txt', 'danmark.txt']
    stop_list = ['er', 'og', 'i', 'et', 'en', 'ei', 'den', 'til', 'på',
                 'de', 'som', 'med', 'for', 'at', 'av', 'fra', 'har', 'om', 'å']
    active_documents = read_documents(document_names)

    query = " halvy en geografisk"

    index = InvertedIndex()
    normalizer = Normalizer()
    search_engine = SearchEngine(index)
    compressor = Compressor(stop_list)

    print("Building index...")
    print("Normalizing terms for space efficiency...")
    print("Stemming terms for space efficiency...")
    # normalize terms and build inverted index
    for document in active_documents:
        normalized_tokens = normalizer.normalize(document.get_tokens())
        # stemmed_tokens = normalizer.stem(normalized_tokens)
        index.build_index(document.doc_id, normalized_tokens)

    print("index", index)

    print("compressing index...")
    size_before = len(index)
    compressor.compress_inverted_index_stop_words(index)
    improvement = round(size_before/(size_before-len(index)), 0)
    print(
        f"removed {size_before-len(index)} posting lists {improvement}% of the index")

    print("Searching...")
    res = search_engine.search(query, "AND")
    print("Matches:", res)
    res = search_engine.get_doc_names(res, active_documents)
    print("Matches:", res)
