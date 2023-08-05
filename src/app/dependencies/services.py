from fastapi import Depends

from app.dependencies.repository import get_sent_email_repository
from app.repositories.sent_email_repository import SentEmailRepository
from app.services.sent_email_service import SentEmailService


def get_sent_email_service(repository: SentEmailRepository = Depends(get_sent_email_repository)) -> SentEmailService:
    return SentEmailService(repository)
