import math


class Ranker():
    def __init__(self):
        self.name = "Ranker"

    def calculate_log_frequency(self, term_pair: list[str, int]) -> float:
        """
        Calculate the log frequency of a term in a document
        """
        return math.log(term_pair[1], 10) + 1
