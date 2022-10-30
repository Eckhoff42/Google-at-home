# Search-engine-algorithm-collection
A collection of algorithms used in search engines implemented by myself 

## How to run
in main.py change the variables `document_names` to include the documents you want to make searchable.

Change the `query` to decide your search term

```
python3 main.py
```

## Inverted index
Inverted index functionality is created in the `InvertedIndex.py` file. A collection of documents is parsed and posting lists are created. Each list consisting of the term and an ordered list of document_ids containing the term. If a term occurs multiple times in a document there is still only one element in the posting list.
```
"example" -> 8, 11, 22
"term" -> 11, 12
```


Two posting lists can be merged with the `merge_and()` and `merge_or()` functions. the AND and OR operator is used respectively to decide what is included in the result posting list. This can be used to evaluate queries.

## Normalizer
The normalizer is used to combine terms with the same meaning into the same group. By doing this the number of posting-lists is reduces saving space. In addition to this evaluation of queries will be more correct


## Compressor

## Query evaluator

## Ranker
TODO