
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
    active_documents = read_documents(document_names)

    query = "Nordisk"

    index = InvertedIndex()
    normalizer = Normalizer()
    search_engine = SearchEngine(index)

    print("Building index...")

    # normalize terms and build inverted index
    for document in active_documents:
        normalized_tokens = normalizer.normalize(document.get_tokens())
        index.build_index(document.doc_id, normalized_tokens)

    print("Searching...")

    res = search_engine.search_implicit_or(query)
    res = search_engine.get_doc_names(res, active_documents)
    print("Matches:", res)
