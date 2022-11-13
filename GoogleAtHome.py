
import argparse
import os
from Document import Document
from Normalizer import Normalizer
from Ranker import Ranker
from SearchEngine import SearchEngine
from Webcrawler import Webcrawler
from countedInvertedIndex import CountedInvertedIndex


def read_files_in_dir(dir_name: str) -> list[str]:
    documents = []
    for i, filename in enumerate(os.listdir(dir_name)):
        if filename.endswith(".txt"):
            path = dir_name + "/" + filename
            documents.append(Document(i, path))
    return documents


def ranked_search_engine_test(directory, query, operator):
    # initialize objects
    index = CountedInvertedIndex()
    normalizer = Normalizer()
    ranker = Ranker(index)
    search_engine = SearchEngine(index, ranker)

    # initialize variables
    active_documents = read_files_in_dir(directory)
    query = query
    operator = operator

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
        print("\n~Matches (most relevant first)~")
        for i, file_name in enumerate(file_names):
            print("[", round(ranked_documents[i][1], 3), "] https://"+file_name.strip("temp/").replace("_",
                  "/").replace(".tx", ""))


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

    crawler = Webcrawler()
    crawler.crawl(args.seed, args.max_pages)
    print("Crawling complete\n")

    ranked_search_engine_test("temp", args.query, "RANKING")

    print("hello world!")
