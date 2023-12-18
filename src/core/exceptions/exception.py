class BaseException(Exception):
    def __init__(self, error: str, message: str):
        self.error = error
        self.message = message


class DatabaseException(BaseException):
    def __init__(self, error: str, message: str):
        super().__init__(error, message)


class NotFoundException(BaseException):
    def __init__(self, error: str, message: str):
        super().__init__(error, message)
