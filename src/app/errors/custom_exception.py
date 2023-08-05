from http import HTTPStatus
from typing import Optional


class CustomException(Exception):
    code: int
    error_code: int
    error_slug: str
    message: str


class BadGatewayException(Exception):
    code: int = HTTPStatus.BAD_GATEWAY
    error_code: int = HTTPStatus.BAD_GATEWAY
    error_slug: str = 'BAD_GATEWAY'
    message: str = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message: Optional[str]):
        if message:
            self.message = message


class BadRequestException(CustomException):
    code: int = HTTPStatus.BAD_REQUEST
    error_code: int = HTTPStatus.BAD_REQUEST
    error_slug: str = 'BAD_REQUEST'
    message: str = HTTPStatus.BAD_REQUEST.description


class NotFoundException(CustomException):
    code: int = HTTPStatus.NOT_FOUND
    error_code: int = HTTPStatus.NOT_FOUND
    error_slug: str = 'NOT_FOUND'
    message: str = HTTPStatus.NOT_FOUND.description


class ForbiddenException(CustomException):
    code: int = HTTPStatus.FORBIDDEN
    error_code: int = HTTPStatus.FORBIDDEN
    error_slug: str = 'FORBIDDEN'
    message: str = HTTPStatus.FORBIDDEN.description


class UnauthorizedException(CustomException):
    code: int = HTTPStatus.UNAUTHORIZED
    error_code: int = HTTPStatus.UNAUTHORIZED
    error_slug: str = 'UNAUTHORIZED'
    message: str = HTTPStatus.UNAUTHORIZED.description


class UnprocessableEntity(CustomException):
    code: int = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code: int = HTTPStatus.UNPROCESSABLE_ENTITY
    error_slug: str = 'UNPROCESSABLE_ENTITY'
    message: str = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DuplicateValueException(CustomException):
    code: int = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code: int = HTTPStatus.UNPROCESSABLE_ENTITY
    error_slug: str = 'UNPROCESSABLE_ENTITY'
    message: str = HTTPStatus.UNPROCESSABLE_ENTITY.description
