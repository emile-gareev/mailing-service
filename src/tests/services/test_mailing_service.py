import sqlalchemy as sa
from base64 import b64encode
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SentEmail
from app.services.sent_email_service import SentEmailService
from tests.constants import INIT_CREATE_COUNT


async def _get_sent_email_from_db(db_session: AsyncSession):
    db_result = await db_session.execute(sa.select(SentEmail))
    db_sent_email = db_result.fetchone()[0]
    assert db_sent_email
    return db_sent_email


async def test_list_sent_emails(sent_email_service: SentEmailService):
    sent_emails_count = await sent_email_service.get_sent_emails_count()
    assert sent_emails_count == INIT_CREATE_COUNT

    all_sent_emails = await sent_email_service.list_sent_emails(page=1, limit=10)
    assert len(all_sent_emails) == INIT_CREATE_COUNT


async def test_get_sent_email(db_session: AsyncSession, sent_email_service: SentEmailService):
    db_sent_email = await _get_sent_email_from_db(db_session)

    sent_email_from_service = await sent_email_service.get_sent_email(db_sent_email.id)
    assert sent_email_from_service
    assert sent_email_from_service.id == db_sent_email.id


async def test_create_sent_email(db_session: AsyncSession, sent_email_service: SentEmailService):
    recipient_list = ['test@test.com', 'test@tst.com', 'tst@other.pl']
    create_data = {
        'subject': 'new_test',
        'recipients': [b64encode(email.encode('utf-8')).decode() for email in recipient_list],
    }

    created_sent_email = await sent_email_service.create_sent_email(create_data)
    assert created_sent_email
