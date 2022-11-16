
import argparse
import os
from Document import Document
from Normalizer import Normalizer
from Ranker import Ranker
from SearchEngine import SearchEngine
from Webcrawler import Webcrawler
from CountedInvertedIndex import CountedInvertedIndex


def read_files_in_dir(dir_name: str) -> list[Document]:
    documents = []
    for i, filename in enumerate(os.listdir(dir_name)):
        if filename.endswith(".txt"):
            path = dir_name + "/" + filename
            documents.append(Document(i, path))
    return documents


def ranked_search_engine_test(directory: str, query: str, operator: str, nr_of_results: int = 10):
    # initialize objects
    index = CountedInvertedIndex()
    normalizer = Normalizer()
    ranker = Ranker(index)
    search_engine = SearchEngine(index, ranker)

    # # initialize variables
    # active_documents = read_files_in_dir(directory)
    # for document in active_documents:
    #     print(document.doc_id)
    # query = query
    # operator = operator

    # print(f"Building index of {len(active_documents)} documents...")
    # print("Normalizing terms for space efficiency...")
    # for document in active_documents:
    #     normalized_tokens = normalizer.normalize(document.get_tokens())
    #     index.build_index(document.doc_id, normalized_tokens)

    # original_index = index.index
    # original_term_frequency = index.term_frequency
    # original_document_frequency = index.document_frequency

    # print(len(original_index), len(original_term_frequency),
    #       len(original_document_frequency))

    # index.write_index_to_file("save/index.txt")
    ind = index.read_index_from_file("save/index.txt")
    # index.write_document_frequency_to_file("save/df.txt")
    df = index.read_document_frequency_from_file("save/df.txt")
    # index.write_term_frequency_to_file("save/tf.txt")
    tf = index.read_term_frequency_from_file("save/tf.txt")
    # index.save_document_names("save/doc_names.txt", active_documents)
    ad = index.read_document_names("save/doc_names.txt")
    print("Normalizing query...")
    normalized_query = normalizer.normalize(query.split())
    print("Executing query...")
    print(f"query = {normalized_query}")
    ranked_documents = search_engine.rank_search_all(
        normalized_query)

    print(ranked_documents)
    results = [ranked_document[0] for ranked_document in ranked_documents]

    if (len(results) == 0):
        print("No results found")
    else:
        file_names = search_engine.get_doc_names(results, ad)
        print(file_names)
        print("\n~Matches (most relevant first)~")
        for i, file_name in enumerate(file_names):
            if i >= nr_of_results:
                break
            print("[", round(ranked_documents[i][1], 3), "] https://"+file_name.strip("temp/").replace("_",
                  "/").replace(".txt", ""))


def init_argparser():
    parser = argparse.ArgumentParser(
        description='Crawl the web `p` pages, then query the results',
        usage='python GoogleAtHome.py [query] [seed] [max_pages]'
    )
    parser.add_argument('-q', '--query', type=str,
                        help='the query to search for')
    parser.add_argument('-s', '--seed', type=str,
                        help='the url to start crawling from')
    parser.add_argument("-p", '--max_pages', type=int,
                        help='the maximum number of pages to crawl')

    return parser.parse_args()


if __name__ == "__main__":
    args = init_argparser()

    # crawler = Webcrawler()
    # crawler.crawl(args.seed, args.max_pages)
    # print("Crawling complete\n")

    ranked_search_engine_test("temp", args.query, "RANKING", 5)
