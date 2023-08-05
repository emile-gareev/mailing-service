import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func

from app.constants import DEFAULT_FROM_EMAIL
from app.db.models.base import Base


class SentEmail(Base):
    """Sent mails info."""

    __tablename__ = 'sent_emails'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True, index=True)  # noqa: A003, VNE003
    subject = sa.Column(sa.String(250), nullable=True)
    recipients = sa.Column(ARRAY(sa.String))
    recipient_count = sa.Column(sa.Integer, default=0)
    sent_at = sa.Column(sa.DateTime(timezone=True), default=func.now())
    from_email = sa.Column(sa.String(64), default=DEFAULT_FROM_EMAIL)
