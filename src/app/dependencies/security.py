import typing as t
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.dependencies.repository import get_service_user_repository
from app.errors.security import BasicAuthUnauthorizedHTTPException
from app.repositories.security import ServiceUserRepository, ServiceUserSchema
from app.utils.security import validate_password

security = HTTPBasic()


async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    repository: ServiceUserRepository = Depends(get_service_user_repository),
) -> t.Optional[ServiceUserSchema]:
    """Authorize the current user from the request."""
    current_username, current_password = credentials.username, credentials.password
    current_user = await repository.get_user_by_username(current_username)
    if not (current_user and validate_password(current_password, current_user.password)):
        raise BasicAuthUnauthorizedHTTPException

    return current_user
