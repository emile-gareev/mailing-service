from base64 import b64encode
from http import HTTPStatus
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import DEFAULT_FROM_EMAIL
from app.repositories.sent_email_repository import SentEmailRepository
from tests.constants import API_CREDENTIALS, INIT_CREATE_COUNT, TEST_COUNT


async def test_get_all(async_client: AsyncClient, db_session: AsyncSession, sent_emails_repo: SentEmailRepository):
    no_auth_response = await async_client.request('GET', '/api/v1/sent_email')
    assert no_auth_response.status_code == HTTPStatus.UNAUTHORIZED

    auth_response = await async_client.request('GET', '/api/v1/sent_email', auth=API_CREDENTIALS)
    assert auth_response.status_code == HTTPStatus.OK

    sent_emails_in_db = await sent_emails_repo.get_all()
    auth_response_data = auth_response.json()

    assert auth_response_data['count'] == len(sent_emails_in_db)


async def test_get_by_id(async_client: AsyncClient, sent_emails_repo: SentEmailRepository):
    sent_emails = await sent_emails_repo.get_all()
    assert sent_emails[0]

    sent_email_id: int = sent_emails[1].id

    no_auth_response = await async_client.request('GET', '/api/v1/sent_email/401')
    assert no_auth_response.status_code == HTTPStatus.UNAUTHORIZED

    ok_response = await async_client.request('GET', f'/api/v1/sent_email/{sent_email_id}', auth=API_CREDENTIALS)
    assert ok_response.status_code == HTTPStatus.OK

    not_found_response = await async_client.request('GET', '/api/v1/sent_email/404', auth=API_CREDENTIALS)
    assert not_found_response.status_code == HTTPStatus.NOT_FOUND


async def test_counter(async_client: AsyncClient):
    # imitation of creation of record from the outside
    recipient_list = ['test@test.com', 'test@tst.com', 'tst@other.pl']
    create_data = {
        'subject': 'new_test',
        'recipients': [b64encode(email.encode('utf-8')).decode() for email in recipient_list],
        'from_email': DEFAULT_FROM_EMAIL,
    }
    response = await async_client.request('POST', '/api/v1/sent_email/', auth=API_CREDENTIALS, json=create_data)
    assert response.status_code == HTTPStatus.CREATED

    # imitation of reading counter from the outside
    response = await async_client.request('GET', '/api/v1/sent_email/month_counter', auth=API_CREDENTIALS)
    assert response.json() == {'recipient_count': INIT_CREATE_COUNT * TEST_COUNT + 2}
