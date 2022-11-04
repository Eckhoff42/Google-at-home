from InvertedIndex import InvertedIndex


class Compressor():
    def __init__(self) -> None:
        self.stop_list = ['er', 'og', 'i', 'et', 'en', 'ei', 'den', 'til', 'på',
                          'de', 'som', 'med', 'for', 'at', 'av', 'fra', 'har', 'om', 'å']

    def compress_inverted_index_stop_words(self, inverted_index: InvertedIndex) -> None:
        """
        Compresses the inverted index by removing stop words.
        These are common words that carry little meaning
        """
        del_terms = []
        for term in inverted_index.index.keys():
            if term in self.stop_list:
                del_terms.append(term)

        for term in del_terms:
            del inverted_index.index[term]

    def remove_stop_words(self, string: str):
        new_string = ""
        for term in string.split():
            if term not in self.stop_list:
                new_string += " " + term

        return new_string

    def gap_encode(self, postings: list) -> list:
        """
        Encodes a postings list using gap encoding
        """
        encoded_postings = []
        for i in range(len(postings)):
            if i == 0:
                encoded_postings.append(postings[i])
            else:
                encoded_postings.append(postings[i] - postings[i-1])

        return encoded_postings

    def gap_decode(self, postings: list, index: int) -> int:
        """
        finds the document id of a posting at index `index` in a gap encoded postings list
        """
        s = 0
        for i in range(index):
            s += postings[i]

        return s + postings[index]

    def encode_variable_byte(self, number: int) -> str:
        """
        Encodes a number using variable bit encoding
        """
        # binary datatype
        binary = bin(number)[2:]

        # number of byte needed
        byte_count = len(binary) / 7
        byte_count = int(byte_count) + (byte_count % 1 > 0)

        encoded_string = ""
        # add all but the last byte'
        zeros = 0
        for i in range(byte_count-1):
            if i == 0 and len(binary) % 7 != 0:
                zeros = (7 - len(binary) % 7)
                encoded_string += "0" + zeros * "0" + binary[:len(binary) % 7]

            else:
                encoded_string += "0" + binary[((i*7)-zeros):((i+1)*7)-zeros]

        # add the last byte
        if len(binary) < 7:
            encoded_string += "1" + (7 - len(binary)) * "0" + binary
        else:
            encoded_string += "1" + binary[-7:]

        return encoded_string

    def decode_variable_byte(self, encoded_string: str) -> int:
        """
        Decodes a variable bit encoded string
        """
        byte_count = len(encoded_string) / 8
        byte_count = int(byte_count) + (byte_count % 1 > 0)

        decoded_string = ""
        for i in range(byte_count):
            decoded_string += encoded_string[i*8+1:i*8+8]

        return int(decoded_string, 2)

    def gamma_encode(self, gap: int) -> str:
        """
        Encodes a number using gamma encoding
        """
        binary = bin(gap)[3:]
        print(binary)
        zeros = len(binary)

        return zeros * "1" + "0" + binary

    def gamma_decode(self, encoded_string: str) -> int:
        """
        Decodes a gamma encoded string
        """
        zeros = 0
        for i in range(len(encoded_string)):
            if encoded_string[i] == "0":
                break
            zeros += 1

        return int("1" + encoded_string[zeros+1:], 2)
