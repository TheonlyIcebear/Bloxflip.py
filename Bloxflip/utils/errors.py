class errors:
    def __init__() -> None:
        pass

    class InsufficientFunds(Exception):
        """Raised if user lacks the funds to do a certain action"""

        pass

    class InvalidAuthorization(Exception):
        """Raised if an invalid Authorization Token is passed"""

        pass

    class GameAlreadyStarted(Exception):
        """Raised if there is an already active game"""

        pass

    class GameNotStarted(Exception):
        """Raised if there is no active game"""

        pass

    class Ratelimited(Exception):
        """Raised if user is ratelimited"""

        pass

    class InvalidParameter(Exception):
        """Raised if an invalid parameter is passed"""

        pass

    class GeneralError(Exception):
        """Raised on a general failures"""

        pass

    class NetworkError(Exception):
        """Raised on cloudflare or other network errors"""

        pass
