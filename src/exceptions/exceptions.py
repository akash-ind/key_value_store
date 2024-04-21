class InvalidCommandException(Exception):

    def __init__(self, message="Invalid Command"):
        super().__init__(message)
