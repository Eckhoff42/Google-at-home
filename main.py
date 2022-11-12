
import argparse
import os
from xmlrpc.client import boolean
from Compressor import Compressor
from Normalizer import Normalizer
from Document import Document
from InvertedIndex import InvertedIndex
from Ranker import Ranker
from SearchEngine import SearchEngine
from countedInvertedIndex import CountedInvertedIndex


def read_files_in_dir(dir_name: str) -> list[str]:
    documents = []
    for i, filename in enumerate(os.listdir(dir_name)):
        if filename.endswith(".txt"):
            path = dir_name + "/" + filename
            documents.append(Document(i, path))
    return documents


def check_args(args):
    if not os.path.isdir(args.directory):
        print(f"The directory '{args.directory}' does not exist")
        exit(1)
    for filename in os.listdir(args.directory):
        if filename.endswith(".txt"):
            return
    print(f"The directory '{args.directory}' does not contain any .txt files")
    exit(1)


def simple_search_engine_test(args):
    # initialize objects
    index = InvertedIndex()
    normalizer = Normalizer()
    search_engine = SearchEngine(index)
    compressor = Compressor()

    # initialize variables
    active_documents = read_files_in_dir(args.directory)
    query = args.query
    operator = args.operator

    print(f"Building index of {len(active_documents)} documents...")
    print("Normalizing terms for space efficiency...")
    print("Stemming terms for space efficiency...")
    for document in active_documents:
        normalized_tokens = normalizer.normalize(document.get_tokens())
        # stemmed_tokens = normalizer.stem(normalized_tokens)
        index.build_index(document.doc_id, normalized_tokens)

    print(index)
    print("compressing index...")
    size_before = len(index)
    compressor.compress_inverted_index_stop_words(index)
    improvement = round(size_before/(size_before-len(index)), 0)
    print(
        f"removed {size_before-len(index)} posting lists {improvement}% of the index")

    print(f"Searching with operator {operator}...")
    query = compressor.remove_stop_words(query)
    normalized_query = normalizer.normalize(query.split())
    results = []
    if (operator in ["AND", "OR"]):
        results = search_engine.search(normalized_query, operator=operator)
    elif (operator == "N_OF_M"):
        results = search_engine.search_n_of_m(
            query, match_percentage=0.5)

    # show results
    if (len(results) == 0):
        print("No results found")
    else:
        file_names = search_engine.get_doc_names(results, active_documents)
        print("Matches:", file_names)


def ranked_search_engine_test(args):
    # initialize objects
    index = CountedInvertedIndex()
    normalizer = Normalizer()
    ranker = Ranker(index)
    search_engine = SearchEngine(index, ranker)
    compressor = Compressor()

    # initialize variables
    active_documents = read_files_in_dir(args.directory)
    query = args.query
    operator = args.operator

    print(f"Building index of {len(active_documents)} documents...")
    print("Normalizing terms for space efficiency...")
    for document in active_documents:
        normalized_tokens = normalizer.normalize(document.get_tokens())
        index.build_index(document.doc_id, normalized_tokens)

    print("Normalizing query...")
    normalized_query = normalizer.normalize(query.split())
    print("Executing query...")
    ranked_documents = search_engine.rank_search(
        normalized_query, active_documents)

    results = [ranked_document[0] for ranked_document in ranked_documents]
    if (len(results) == 0):
        print("No results found")
    else:
        file_names = search_engine.get_doc_names(results, active_documents)
        print("~Matches (most relevant first)~\n", file_names)


if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser(
        description="Search Engine for a given set of documents",
        usage="python3 main.py -dir < directory-name > -q < query > -o < operator >")
    parser.add_argument("-dir", "--directory", type=str,
                        required=False, default="corpus",)
    parser.add_argument("-q", "--query", type=str, required=True,)
    parser.add_argument("-o", "--operator", type=str,
                        required=False, default="AND", choices=["AND", "OR", "N_OF_M", "RANKING"],)

    args = parser.parse_args()
    check_args(args)

    if (args.operator == "RANKING"):
        ranked_search_engine_test(args)
    else:
        simple_search_engine_test(args)
