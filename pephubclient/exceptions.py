class IncorrectQueryStringError(Exception):
    def __init__(self, query_string: str = None):
        self.query_string = query_string
        super().__init__(
            f"PEP data with passed namespace and project ({self.query_string}) name not found."
        )
