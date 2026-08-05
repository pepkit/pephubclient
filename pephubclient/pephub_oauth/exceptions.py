"""Auth exceptions."""


class PEPHubResponseException(Exception):
    """Request response exception. Used when response != 200."""

    def __init__(self, reason: str = "") -> None:
        """
        Optionally provide explanation for the exceptional condition.

        Args:
            reason: Some context or perhaps just a value that could not be
                interpreted as an accession.
        """
        super().__init__(reason)


class PEPHubTokenExchangeException(Exception):
    """Exception in exchanging device code for token == 400."""

    def __init__(self, reason: str = "") -> None:
        """
        Optionally provide explanation for the exceptional condition.

        Args:
            reason: Some context or perhaps just a value that could not be
                interpreted as an accession.
        """
        super().__init__(reason)
