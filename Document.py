class Document():
    """
    Simple document class that stores the document ID and the content.
    """

    def __init__(self, doc_id: int, fileName: str) -> None:
        self.doc_id: int = doc_id
        self.fileName: str = fileName

    def __str__(self):
        return f"Document {self.doc_id}:\n{self.content}"

    def get_tokens(self) -> list[str]:
        return open(self.fileName).read().split()
