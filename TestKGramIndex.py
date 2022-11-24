from KGramIndex import KGramIndex


if __name__ == '__main__':
    index = KGramIndex()

    string = "hello helpful lovley full hate happy hellomate"
    index.index_terms(string.split())
    print(index)
    r = index.evaluate("hello")
    print(r)
