class Document():
    """
    Simple document class that stores the document ID and the content.
    """

    def __init__(self, doc_id: int, content: str, fileName: str) -> None:
        self.doc_id: int = doc_id
        self.content: str = content
        self.fileName: str = fileName

    def __str__(self):
        return f"Document {self.doc_id}:\n{self.content}"

    def get_tokens(self) -> list[str]:
        return self.content.split()
