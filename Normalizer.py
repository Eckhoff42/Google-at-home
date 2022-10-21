import re


class Normalizer():
    """
    Simple document class that stores the document ID and the content.
    """

    def __init__(self):
        pass

    def normalize_term(self, content: str) -> str:
        # remove everything between brackets
        c = re.sub(r'\[.*?\]', '', content.lower())
        # remove everything that is not a letter
        c = re.sub(r'[^a-z]', '', c)
        return c

    def normalize(self, terms: list[str]) -> list[str]:
        for i, term in enumerate(terms):
            terms[i] = self.normalize_term(term)

        return terms
