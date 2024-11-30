class EntityNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class EntityAlreadyExistsException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
