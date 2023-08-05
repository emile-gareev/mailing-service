from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, message: str = 'Not found') -> None:
        super().__init__(status_code=404, detail={'code': 'NOT_FOUND', 'message': message})


class MaskedError:
    def __init__(self, original: Exception) -> None:
        self.__original = original

    @property
    def original(self) -> Exception:
        return self.__original


class UnexpectedError(MaskedError, HTTPException):
    def __init__(self, original: Exception) -> None:
        MaskedError.__init__(self, original)
        HTTPException.__init__(
            self,
            status_code=400,
            detail={
                'code': 'UNEXPECTED_ERROR',
                'message': f'[{type(original).__name__}] {original}',
            },
        )


class LimitChangeError(HTTPException):
    def __init__(self, message: str = 'New limit value must be greater than the current one') -> None:
        super().__init__(status_code=400, detail={'code': 'LIMIT_MUST_BE_GRATER', 'message': message})


class NotReadyBatchError(HTTPException):
    def __init__(self, message: str = 'Batch not in incorrect status! Try again later.') -> None:
        super().__init__(status_code=400, detail={'code': 'BATCH_NOT_READY', 'message': message})
