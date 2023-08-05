import sqlalchemy as sa
import typing as t
from datetime import datetime
from sqlalchemy import and_

from app.db.models import SentEmail
from app.repositories.base import BasicRepository
from app.routers.internal.v1.filters import SentEmailFilter
from app.routers.internal.v1.schemas import SentEmailSchema


class SentEmailRepository(BasicRepository):
    """Repository for working with sent emails."""

    async def create_sent_email(self, create_data) -> int:
        result = await self._session.execute(
            sa.insert(SentEmail).values(**create_data),
        )
        return result.inserted_primary_key[0]

    async def get_all(self, page: int = 1, limit: t.Optional[int] = 10, filtering: SentEmailFilter = None):
        """Get all emails with filtering, sorting and pagination applied."""
        query = sa.select(SentEmail).distinct()

        if filtering:
            query = filtering.filter(query)
            query = filtering.sort(query)

        if page and limit:
            offset = (page - 1) * limit
            query = query.limit(limit).offset(offset)

        result = await self._session.execute(query)
        return result.unique().scalars().all()

    async def get_by_id(self, sent_email_id: int, return_schema=True) -> t.Optional[SentEmailSchema]:
        query = sa.select(SentEmail).where(SentEmail.id == sent_email_id)
        result = await self._session.scalars(query)
        sent_email = result.first()

        if sent_email and return_schema:
            return SentEmailSchema.from_orm(sent_email)

        return sent_email

    async def count_emails_total(self, filtering: SentEmailFilter = None):
        """Get all emails count with filtering applied."""
        query = sa.select(sa.func.count(sa.distinct(SentEmail.id))).select_from(SentEmail)

        if filtering:
            query = filtering.filter(query)

        result = await self._session.execute(query)
        return result.scalar()

    async def _get_count_result(self, condition, from_email, filtering: SentEmailFilter = None):
        """Calculate the amount of recipients in the current month."""
        query = sa.select(sa.func.sum(condition)).where(
            and_(sa.extract('month', SentEmail.sent_at) == datetime.now().month, SentEmail.from_email == from_email)
        )

        if filtering:
            query = filtering.filter(query)

        result = await self._session.execute(query)
        count = result.scalar()
        return count if count else 0

    async def count_recipient_per_month(self, from_email, filtering: SentEmailFilter = None):
        return await self._get_count_result(SentEmail.recipient_count, from_email, filtering)
