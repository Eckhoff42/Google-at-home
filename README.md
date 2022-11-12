# Search-engine-algorithm-collection
A collection of algorithms used in search engines implemented by myself. The intention of this project is not to implement the most effective algorithms, but to implement a variety of techniques.
The selection of algorithms are inspired from the Stanford course [Introduction to Information Retrieval](https://web.stanford.edu/class/cs276/)
## Table of contents
- [Search-engine-algorithm-collection](#search-engine-algorithm-collection)
  - [Table of contents](#table-of-contents)
  - [How to run](#how-to-run)
  - [Inverted index](#inverted-index)
  - [Normalizer](#normalizer)
    - [normalizing operations](#normalizing-operations)
    - [Stemming](#stemming)
  - [Compressor](#compressor)
    - [Gap encoding](#gap-encoding)
    - [Variable byte encoding](#variable-byte-encoding)
    - [Gamma encoding](#gamma-encoding)
  - [Search engine](#search-engine)
    - [Search(operator = "AND"):](#searchoperator--and)
    - [Search(operator = "AND"):](#searchoperator--and-1)
    - [Search_n_of_m():](#search_n_of_m)
  - [Ranker](#ranker)

## How to run
Leave the files you want to index in the `corpus/` directory. currently only .txt files are indexed. There are currently some demo files in the directory.

run the file
```
python3 main.py --directory corpus --query <your query> --operator <your search operator> 
```
The current operators are:
- AND
- OR
- N_OF_M

the output of the query is a list if file-names including the matches. 

## Inverted index
Inverted index functionality is created in the `InvertedIndex.py` file. A collection of documents is parsed and posting lists are created. Each list consisting of the term and an ordered list of document_ids containing the term. If a term occurs multiple times in a document there is still only one element in the posting list.
```
"example" -> 8, 11, 22
"term" -> 11, 12
```

Two posting lists can be merged with the `merge_and()` and `merge_or()` functions. the AND and OR operator is used respectively to decide what is included in the result posting list. This can be used to evaluate queries.

## Normalizer
The normalizer is used to combine terms with the same meaning into the same group. By doing this the number of posting-lists is reduces saving space. In addition to this evaluation of queries will be more correct as words carrying the same meaning are made equivalent

### normalizing operations
- lowercase: `Example -> example`
- removing non-alphabetic characters: `example[1*] -> example`
- stemming: `ies -> i`

### Stemming
 is performed using a simplified *Porter stemming algorithm*. The algorithm is used to truncate different endings of terms into one. By doing this different forms of the same word is transformed into the same. NB: this algorithm is english specific

## Compressor
Compressing the inverted index has multiple benefits. A smaller index uses less memory that allows bigger parts of large indexes to be in memory at the same time. Another benefit is better query evaluation. Normalization is a form of compression where multiple words with the same meaning eg. "do, does, doing" is interpreted as representing the same. This leads to better query evaluation.

The compressor removes stop words eg. "the, and, in, to, one" that are common but bears little meaning in isolation. One side effect of this is removing false positives in query evaluation where "The quick fox" would include all documents including the term "the".

### Gap encoding
TODO

### Variable byte encoding
TODO

### Gamma encoding
TODO

## Search engine
The search engine given a `query` evaluates the string and finds matching documents. What documents are matching depends on how the query is evaluated and multiple search-functions are given.

### Search(operator = "AND"):
after parsing the query normalizing and stemming the terms it looks for documents where all search-terms are present

### Search(operator = "AND"):
after parsing the query normalizing and stemming the terms it looks for documents where at least one search-terms is present

### Search_n_of_m():
after parsing the query normalizing and stemming the terms it looks for documents where at least a specified percentage of the words are present. A `query` consisting of 4 terms and a `match_percentage` of 50% means any document containing at least 2 search terms is a match.

## Ranker
Executing a query using the search engine will return a list of documents that matches the query. The ranker takes this list and ranks the documents based on how relevant they are to the query. The ranker is implemented in the `Ranker.py` file. The relevance of a document `d` for a given term `t` is decided by the term frequency (`tf`).
- $tf(w_{t,d}) = 1 + log_{10}(t,d)$ iff $tf_{t,d} > 0$
- $tf(w_{t,d}) = 0$                 iff $tf_{t,d} > 0$

The more occurrences of a term in a document the more relevant the document is. Further more we wish to give common terms a lower weight and uncommon terms a high weight. This is done by using the inverse document frequency (`idf`).
