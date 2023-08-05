from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_session
from app.repositories.sent_email_repository import SentEmailRepository
from app.repositories.security import ServiceUserRepository


def get_sent_email_repository(session: AsyncSession = Depends(get_session)) -> SentEmailRepository:
    return SentEmailRepository(session)


def get_service_user_repository(session: AsyncSession = Depends(get_session)) -> ServiceUserRepository:
    return ServiceUserRepository(session)
