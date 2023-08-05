import typing as t
from datetime import datetime

from app.db.models import ORJSONModel


class SentEmailSchema(ORJSONModel):
    class Config:
        use_enum_values = True
        orm_mode = True

    id: int  # noqa: A003, VNE003
    subject: t.Optional[str]
    recipients: t.List[str]
    recipient_count: int
    sent_at: t.Optional[datetime]
    from_email: t.Optional[str]


class SentEmailsListSchema(ORJSONModel):
    count: int
    results: t.List[SentEmailSchema]


class SentEmailInputSchema(ORJSONModel):
    subject: t.Optional[str]
    recipients: t.List[str]
    from_email: t.Optional[str]


class CounterSchema(ORJSONModel):
    class Config:
        orm_mode = True

    recipient_count: int
