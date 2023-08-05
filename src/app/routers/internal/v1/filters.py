import typing as t
from datetime import datetime
from fastapi_filter.contrib.sqlalchemy import Filter

from app.db.models import SentEmail


class SentEmailFilter(Filter):
    """Filtering the sent email model."""
    id: t.Optional[int]  # noqa

    subject__ilike: t.Optional[str]
    recipients__ilike: t.Optional[str]
    recipient_count: t.Optional[int]
    sent_at: t.Optional[datetime]

    ordering: t.Optional[list[str]] = ['-sent_at']
    common_search: t.Optional[str]

    class Constants(Filter.Constants):
        model = SentEmail
        ordering_field_name = 'ordering'
        search_field_name = 'common_search'
        search_model_fields = ['subject']
