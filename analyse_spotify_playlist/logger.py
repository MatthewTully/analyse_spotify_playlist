"""Simple Log class."""


class Log:
    """Log class"""

    log_messages = False

    def __init__(self) -> None:
        pass

    def print(self, message: str) -> None:
        """Print message to console if logging is allowed."""
        if Log.log_messages:
            print(message)

    def set_logger(self, verbose: bool) -> None:
        """Change log_message flag."""
        Log.log_messages = verbose
