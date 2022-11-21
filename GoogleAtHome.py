
import argparse
import os
from Document import Document
from Normalizer import Normalizer
from Ranker import Ranker
from SearchEngine import SearchEngine
from Webcrawler import Webcrawler
from CountedInvertedIndex import CountedInvertedIndex


def print_results(ranked_documents: list[tuple[int, float]], active_documents: list[Document], nr_of_results: int = 10):
    results = [ranked_document[0] for ranked_document in ranked_documents]

    if (len(results) == 0):
        print("No results found")
    else:
        s = SearchEngine(None, None)
        file_names = s.get_doc_names(results, active_documents)
        print("\n~Matches (most relevant first)~")

        for i, file_name in enumerate(file_names):
            if i >= nr_of_results:
                break

            score = round(ranked_documents[i][1], 3)
            url = file_name.strip().replace(
                "temp/", "").replace(".txt", "").replace("\\", "/")
            print(f"[ {score} ] {url}")


def read_files_in_dir(dir_name: str) -> list[Document]:
    documents = []
    for i, filename in enumerate(os.listdir(dir_name)):
        if filename.endswith(".txt"):
            path = dir_name + "/" + filename
            documents.append(Document(i, path))
    return documents


def save(index: CountedInvertedIndex, active_documents: list[Document]):
    index.write_index_to_file("save/index.txt")
    index.write_document_frequency_to_file("save/df.txt")
    index.write_term_frequency_to_file("save/tf.txt")
    index.save_document_names("save/doc_names.txt", active_documents)


def load():
    index = CountedInvertedIndex()
    index.read_index_from_file("save/index.txt")
    index.read_document_frequency_from_file("save/df.txt")
    index.read_term_frequency_from_file("save/tf.txt")

    return index


def crawl_to_file(seed, max_pages):
    # initialize directories "save" and "temp"
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists("save"):
        os.mkdir("save")

    for file in os.listdir("temp"):
        os.remove("temp/" + file)
    for file in os.listdir("save"):
        os.remove("save/" + file)

    crawler = Webcrawler()
    index = CountedInvertedIndex()
    normalizer = Normalizer()

    print("Crawling...")
    crawler.crawl(seed, max_pages)
    print("Crawling complete")

    active_documents = read_files_in_dir("temp")
    for document in active_documents:
        normalized_tokens = normalizer.normalize(document.get_tokens())
        index.build_index(document.doc_id, normalized_tokens)

    save(index, active_documents)


def test(query: str, nr_of_results: int = 10):
    print("Loading index from files...")
    index = load()
    active_documents = index.read_document_names("save/doc_names.txt")
    normalizer = Normalizer()
    ranker = Ranker(index)
    search_engine = SearchEngine(index, ranker)

    print("Normalizing query...")
    normalized_query = normalizer.normalize(query.split())
    print("Executing query...")
    print(f"query = {normalized_query}")
    ranked_documents = search_engine.rank_search_all(normalized_query)
    print_results(ranked_documents, active_documents, nr_of_results)


def init_argparser():
    parser = argparse.ArgumentParser(
        description='Crawl the web `p` pages, then query the results',
        usage='python GoogleAtHome.py [query] [seed] [max_pages]'
    )
    parser.add_argument('-q', '--query', type=str,
                        help='the query to search for')
    parser.add_argument('-r', '--results', type=int, default=10)
    parser.add_argument('-s', '--seed', type=str,
                        help='the url to start crawling from')
    parser.add_argument("-p", '--max_pages', type=int, default=10,
                        help='the maximum number of pages to crawl')

    return parser.parse_args()


if __name__ == "__main__":
    args = init_argparser()

    if args.seed:
        crawl_to_file(args.seed, args.max_pages)

    test(args.query, args.results)
