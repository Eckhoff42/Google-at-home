# Search-engine-algorithm-collection
A collection of algorithms used in search engines implemented by myself. The intention of this project is not to implement the most effective algorithms, but to implement a variety of techniques.
The selection of algorithms are inspired from the Stanford course [Introduction to Information Retrieval](https://web.stanford.edu/class/cs276/)
## Table of contents
- [Search-engine-algorithm-collection](#search-engine-algorithm-collection)
  - [Table of contents](#table-of-contents)
  - [Structure](#structure)
  - [How to run google at home](#how-to-run-google-at-home)
  - [How to run search engine](#how-to-run-search-engine)
  - [How to run the crawler](#how-to-run-the-crawler)
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
    - [Query evaluation](#query-evaluation)
  - [Web crawler](#web-crawler)
    - [The standard process](#the-standard-process)

## Structure

![image](https://user-images.githubusercontent.com/42439472/201487558-6476ee53-3823-4ed9-9203-ff71065b7d96.png)

## How to run google at home
Run google at home with the command:
```
python3 GoogleAtHome.py <query> <seed> <max_pages>
```
- query: the query you want to search
- seed: the url of the seed page
- max_pages: the maximum number of pages you want to crawl

This will crawl the web starting at \<seed> The text content of the pages will be saved to the `temp` directory. The search engine will then be built on the crawled pages. The results will be printed to the console ranked according to tf-idf.


## How to run search engine
Leave the files you want to index in the `corpus/` directory. currently only .txt files are indexed. There are currently some demo files in the directory.

run the file
```
python3 main.py --directory corpus --query <your query> --operator <your search operator> 
```
The current operators are:
- AND
- OR
- N_OF_M
- RANKING

the output of the query is a list of file-names.

## How to run the crawler
The crawler can be run with the command:
```
python3 crawler.py <url> <max_pages>
```
- seed: the url of the seed page
- max_pages: the maximum number of pages you want to crawl

this will crawl the web starting at \<seed> The text content of the pages will be saved to the `temp` directory.

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
A compression technique used to reduce the size of the inverted index. The idea is to store the difference between two following document_ids in the posting list instead of the actual document_id. Decoding a document_id is done by adding the values of all previous elements in the gap encoded list

**Before**
```
"secondTerm" -> 11, 12
"firstTerm" -> 1, 2, 3, 8, 11
```
**After**
```
"secondTerm" -> 11,1
"firstTerm" -> 1,1,1,5,3
# decoding this -----^
# is done by 1+1+1+5 = 8
```



### Variable byte encoding
A compression technique used to allow a buffer to contain numbers of different sizes. In our case the smallest unit is 1 byte (8bit).
The first bit of each byte is used to signify if the byte is the last byte in the sequence. The remaining 7 bits are used to store the value of the number. 

**encoding a number**
```
1. transform the number into binary
  - 480 = 1101001011
2. split the binary into 7 bit chunks
  - 110 1001011
3. add trailing zeros to the first byte
  - 0000110 1001011
4. add a 0 to the first bit all but the last byte with a 1
  - 00000110 11001011
```
**decoding a byte string**
```
byteString = 00000110 11001011 10001010
1. read bytes until the first byte with a 1 in the first bit is found
  - 00000110 11001011
2. remove the first bit from all bytes
  - 0000110 1001011
3. remove trailing zeros from the first byte
  - 1101001011
```

### Gamma encoding
A compression technique used to allow a buffer to contain numbers of different sizes. A gamma encoded number is represented as a combination of offset and length.
- offset: the number in binary with the leading 1 cut off
- length: the length of the offset in unary

**encoding a number**
```
1. create offset and length
  - offset: 13 -> 1101 -> 101
  - length: 3 -> 1110
2. create gamma encoded number
  - 1110101
```

## Search engine
The search engine given a `query` evaluates the string and finds matching documents. What documents are matching depends on how the query is evaluated and multiple search-functions are given.

### Search(operator = "AND"):
after parsing the query normalizing and stemming the terms it looks for documents where all search-terms are present

### Search(operator = "AND"):
after parsing the query normalizing and stemming the terms it looks for documents where at least one search-terms is present

### Search_n_of_m():
after parsing the query normalizing and stemming the terms it looks for documents where at least a specified percentage of the words are present. A `query` consisting of 4 terms and a `match_percentage` of 50% means any document containing at least 2 search terms is a match.

## Ranker
Executing a query using the search engine will return a list of documents that matches the query. The ranker takes this list and ranks the documents based on how relevant they are to the query. The ranker is implemented in the `Ranker.py` file. The relevance of a document `d` for a given term `t` is decided by the log of term frequency (`tf`).
- $w_{t,d} = 1 + log_{10}(t,d)$ iff $tf_{t,d} > 0$
- $w_{t,d} = 0$                 iff $tf_{t,d} > 0$

The more occurrences of a term in a document the more relevant the document is. Further more we wish to give common terms a lower weight and uncommon terms a high weight. This is done by weighting the term frequency with the inverse document frequency (`idf`).
- $idf_{t} = log_{10}\frac{N}{df_{t}}$
- document frequency (`df`) is the number of documents containing the term
- N is the total number of documents

The weight of a term `t` for a document `d` is then
- $w_{t,d} = log_{10}(1+ tf_{t,d}) * log_{10}\frac{N}{df_{t}}$

Scoring a document `d` for a query `q` is done by summing the weights of all terms in the query for the document.
- $score_{d,q} = \sum_{t \in q} w_{t,d}$

### Query evaluation
One naive solution of evaluating a query is to calculate the score for each document and return the documents with the highest score. This is however not optimal as it requires calculating the score for all documents. A better solution is to only calculate the score for documents that matches the query. This is done by using the inverted index to find documents that matches the query. The documents are then ranked by calculating the score for each document. Other techniques can be used to reduce the number of documents that needs to be ranked, but they are not implemented in this project (yet). 

## Web crawler
A web crawler commonly referred to as spiders is a program used to index the internet. It reads the content of a website and extracts links to other websites. The crawler then visits the linked websites and repeats the process. The crawler is implemented in the `Crawler.py` file. The crawler is implemented using the `requests` library to fetch the content of a website and the `BeautifulSoup` library to parse the content. 

![image](https://user-images.githubusercontent.com/42439472/201518967-c091e1a9-d255-4c63-a077-64dfa8c503f3.png)

### The standard process
1. Get an url from the queue
2. Register the url as visited
3. Check the robots.txt file to see if the url is allowed to be crawled
   1. first check if the robots.txt is cashed 
   2. if not get the url/robots.txt and parse it
4. Fetch the content of a website
   1. Save the specified to a file
   2. Add all links to the queue if they are not already in the queue
5. Repeat until the n sites have been crawled 
