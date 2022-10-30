import re


class Normalizer():
    """
    Simple document class that stores the document ID and the content.
    """

    def __init__(self):
        pass

    def normalize_term(self, content: str) -> str:
        """
        Normalize a term by non information bearing characters.
        The regex is performed in multiple steps to make it easier to read.
        """
        # remove everything between brackets
        c = re.sub(r'\[.*?\]', '', content.lower())
        # remove everything that is not a letter
        c = re.sub(r'[^a-z]', '', c)
        return c

    def normalize(self, terms: list[str]) -> list[str]:
        for i, term in enumerate(terms):
            terms[i] = self.normalize_term(term)

        return terms

    def stem_term(self, term: str) -> str:
        """
        Stem a term using the a simplified Porter Stemmer algorithm.
        The regex is performed in multiple steps to make it easier to read.
        NB: This only works on english documents.
        """
        c = re.sub(r'ies$', 'i', term)
        c = re.sub(r'sses$', 'ss', term)
        c = re.sub(r'ational$', 'ate', term)
        c = re.sub(r'tional$', 'tion', term)

        return c

    def stem(self, terms: list[str]) -> str:
        """
        Stem all terms in the list using the a simplified Porter Stemmer algorithm.
        """
        for i, term in enumerate(terms):
            terms[i] = self.stem_term(term)

        return terms
