
from Document import Document


def save_document_names(filename: str, active_documents: list[Document]):
    """
    Save the document names to a file
    """
    with open(filename, 'w') as file:
        for document in active_documents:
            file.write(str(document.doc_id) + ": " +
                       document.fileName + "\n")


def read_document_names(filename: str):
    """Read the document names from a file"""
    active_documents = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.split(": ")
            document = int(line[0])
            name = line[1]
            active_documents.append(Document(document, name))

    return active_documents


def save_url_names(filename: str, urls: list[int, str]):
    """
    Save the document names to a file
    """
    with open(filename, 'w') as file:
        for id, url in urls:
            file.write(str(id) + ": " +
                       url + "\n")


def write_index_to_file(index, filename: str):
    """
    Write the index to a file
    """
    with open(filename, 'w') as file:
        for term in index:
            file.write(term + ": ")
            for doc in index[term]:
                file.write(str(doc[0]) + " " + str(doc[1]) + " ")
            file.write("\n")


def read_index_from_file(filename: str):
    """
    Read the index from a file
    """
    copy = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.split(": ")
            term = line[0]
            copy[term] = []
            postings = line[1].split(" ")
            for i in range(0, len(postings) - 1, 2):
                copy[term].append(
                    [int(postings[i]), int(postings[i + 1])])

    return copy


def write_term_frequency_to_file(term_frequency, filename: str):
    """
    Write the term frequency to a file
    """
    with open(filename, 'w') as file:
        for document in term_frequency:
            file.write(str(document) + ": ")
            for term in term_frequency[document]:
                file.write(
                    term + " " + str(term_frequency[document][term]) + " ")
            file.write("\n")


def read_term_frequency_from_file(filename: str):
    """
    Read the term frequency from a file
    """
    copy = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.split(": ")
            document = int(line[0])
            copy[document] = {}
            terms = line[1].split(" ")
            for i in range(0, len(terms) - 1, 2):
                copy[document][terms[i]] = int(terms[i + 1])

    return copy


def write_document_frequency_to_file(document_frequency, filename: str):
    """
    Write the document frequency to a file
    """
    with open(filename, 'w') as file:
        for term in document_frequency:
            file.write(term + ": " +
                       str(document_frequency[term]) + "\n")


def read_document_frequency_from_file(filename: str):
    """
    Read the document frequency from a file
    """
    copy = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.split(": ")
            term = line[0]
            copy[term] = int(line[1])

    return copy


def save_visited(visited, file_name: str):
    with open(file_name, 'w') as f:
        for item in visited:
            f.write("%s\n" % item)


def read_visited(file_name: str):
    visited = []
    with open(file_name, 'r') as f:
        for line in f:
            visited.append(line.strip())

    return visited
