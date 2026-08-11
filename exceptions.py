class CustomError(Exception):
    """Base class for other exceptions."""
    pass

class ValidationError(CustomError):
    """Raised when validation fails."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

class DatabaseError(CustomError):
    """Raised when there's a database error."""
    def __init__(self, message: str, code: int) -> None:
        super().__init__(message)
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"DatabaseError {self.code}: {self.message}"

class NotFoundError(CustomError):
    """Raised when a resource is not found."""
    def __init__(self, resource: str) -> None:
        self.resource = resource
        super().__init__(f'{resource} not found')

    def __str__(self) -> str:
        return f'{self.resource} was not found.'