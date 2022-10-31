
import argparse
import os
from xmlrpc.client import boolean
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


def read_files_in_dir(dir_name: str) -> list[str]:
    # get the file names of documents in the given directory
    documents = []
    for i, filename in enumerate(os.listdir(dir_name)):
        if filename.endswith(".txt"):
            path = dir_name + "/" + filename
            documents.append(Document(i, path))
    return documents

# enum for the different search modes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Search Engine for a given set of documents",
        usage="python3 main.py -dir < directory-name > -q < query > -o < operator >")
    parser.add_argument("-dir", "--directory", type=str, required=True,)
    parser.add_argument("-q", "--query", type=str, required=True,)
    parser.add_argument("-o", "--operator", type=str,
                        required=False, default="AND", choices=["AND", "OR", "N_OF_M"],)
    args = parser.parse_args()

    # initialize objects
    index = InvertedIndex()
    normalizer = Normalizer()
    search_engine = SearchEngine(index)
    compressor = Compressor()

    # initialize variables
    active_documents = read_files_in_dir(args.directory)
    query = args.query
    operator = args.operator

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

    print(f"Searching with operator {operator}...")
    query = compressor.remove_stop_words(query)
    results = []
    if (operator in ["AND", "OR"]):
        results = search_engine.search(query, operator=operator)
    elif (operator == "N_OF_M"):
        results = search_engine.search_n_of_m(
            query, match_percentage=0.5)

    # show results
    if (len(results) == 0):
        print("No results found")
    else:
        file_names = search_engine.get_doc_names(results, active_documents)
        print("Matches:", file_names)
