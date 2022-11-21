from fastapi import FastAPI
import PersistentStorage
from Document import Document
from Normalizer import Normalizer
from Ranker import Ranker
from SearchEngine import SearchEngine
from Webcrawler import Webcrawler
from CountedInvertedIndex import CountedInvertedIndex
app = FastAPI()

index = CountedInvertedIndex()
index.load()
active_documents = PersistentStorage.read_document_names(
    "save/doc_names.txt")
normalizer = Normalizer()
ranker = Ranker(index)
search_engine = SearchEngine(index, ranker)


@app.get("/search")
def hello(query: str, res: int = 100):
    normalized_query = normalizer.normalize(query.split())
    ranked_documents = search_engine.rank_search_all(normalized_query)

    results = [ranked_document[0] for ranked_document in ranked_documents]

    ret = []
    if (len(results) == 0):
        return []
    else:
        s = SearchEngine(None, None)
        file_names = s.get_doc_names(results, active_documents)

        for i, file_name in enumerate(file_names):
            if i >= res:
                break

            score = round(ranked_documents[i][1], 3)
            url = file_name.strip().replace(
                "temp/", "").replace(".txt", "").replace("\\", "/")
            ret.append((score, url))

    return ret
