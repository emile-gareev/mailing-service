import re
import typing as t
from base64 import b64decode
from logging import getLogger

from app.errors.custom_exception import NotFoundException
from app.repositories.sent_email_repository import SentEmailRepository
from app.routers.internal.v1.filters import SentEmailFilter
from app.routers.internal.v1.schemas import SentEmailInputSchema, SentEmailSchema

logger = getLogger(__file__)


class SentEmailService:
    """Service for work with sent emails."""

    def __init__(self, repository: SentEmailRepository) -> None:
        self._repository = repository

    async def get_sent_emails_count(self, filtering: SentEmailFilter = None):
        return await self._repository.count_emails_total(filtering=filtering)

    async def get_recipient_month_count(self, from_email: str, filtering: SentEmailFilter = None):
        return await self._repository.count_recipient_per_month(from_email, filtering=filtering)

    async def list_sent_emails(
            self, page: int, limit: int, filtering: SentEmailFilter = None,
    ) -> t.Optional[SentEmailSchema]:
        return await self._repository.get_all(page, limit, filtering=filtering)

    async def get_sent_email(self, sent_email_id: int):
        sent_email = await self._repository.get_by_id(sent_email_id, return_schema=False)
        if not sent_email:
            raise NotFoundException

        return sent_email

    async def _split_emails_count(self, emails_list, specific_email_regex=None):
        """
        Counting from the list of recipients the number of specific recipients and others.
        :param: email_regex - filter for specific emails like r'@gmail.com'.
        """
        specific_count = None
        other_count = len(emails_list)

        if specific_email_regex:
            specific_count = 0
            other_count = 0

            for email in emails_list:
                if re.search(specific_email_regex, email.lower()):
                    specific_count += 1
                else:
                    other_count += 1

        return specific_count, other_count

    async def create_sent_email(self, email_data: t.Union[SentEmailInputSchema, dict]):
        """
        Recording information on the sent email in the database.
        """
        if isinstance(email_data, SentEmailInputSchema):
            email_dict: dict = email_data.dict()
        else:
            email_dict = email_data

        email_dict['recipients'] = [b64decode(email).decode('utf-8') for email in email_dict.get('recipients')]
        recipient_count = len(set(email_dict.get('recipients')))

        email_dict['recipient_count'] = recipient_count

        sent_email_id = await self._repository.create_sent_email(email_dict)

        return await self.get_sent_email(sent_email_id)
