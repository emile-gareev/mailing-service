import asyncio
import json
import os
import pytest
import random
import sqlalchemy as sa
import string
from aiohttp import web
from aiohttp.test_utils import TestServer
from aiohttp.web import Request, Response
from alembic import command
from alembic.config import Config
from aresponses import ResponsesMockServer
from asyncio import AbstractEventLoop
from httpx import AsyncClient
from pathlib import Path
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from typing import Any, AsyncGenerator, Generator
from yarl import URL

from app.db.connection import get_master_dsn
from app.db.models import SentEmail, ServiceUser
from app.main import app
from app.repositories.sent_email_repository import SentEmailRepository
from app.services.sent_email_service import SentEmailService
from app.utils.security import hash_password
from tests.constants import API_CREDENTIALS, INIT_CREATE_COUNT, TEST_COUNT
from tests.utils import create_database, drop_database


def _run_upgrade(connection: AsyncConnection) -> None:
    base_dir = Path(__file__).resolve().parent.parent
    alembic_cfg = Config(os.path.join(base_dir, 'alembic.ini'))

    alembic_cfg.attributes['connection'] = connection
    command.upgrade(alembic_cfg, 'head')


def _generate_fake_sent_email(count: int):
    emails = [
        ''.join(random.choice(string.ascii_lowercase) for _ in range(5)) + '@test.ru' for _count in range(count)
    ]

    return SentEmail(
        subject='test',
        recipients=emails,
        recipient_count=count,
    )


@pytest.fixture(scope='session', autouse=True)
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def database(event_loop: AbstractEventLoop) -> AsyncGenerator[str, None]:
    db_url = get_master_dsn(is_test=True)
    await create_database(db_url)
    engine = create_async_engine(db_url, poolclass=NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(_run_upgrade)
    await engine.dispose()

    try:
        yield db_url
    finally:
        await drop_database(db_url)


@pytest.fixture(scope='session')
async def sqla_engine(database: str) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(database, poolclass=NullPool)
    yield engine
    await engine.dispose()


@pytest.fixture()
async def db_session(mocker: MockerFixture, sqla_engine: AsyncEngine) -> AsyncSession:
    """
    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.
    """
    connection = await sqla_engine.connect()
    trans = await connection.begin()

    session = AsyncSession(bind=connection, expire_on_commit=False)

    mocker.patch('sqlalchemy.orm.session.sessionmaker.__call__', return_value=session)

    async with session:
        yield session

        await trans.rollback()
        await connection.close()


@pytest.fixture(autouse=True)
async def cleanup(db_session: AsyncSession) -> AsyncGenerator[None, None]:
    yield
    await db_session.execute(sa.delete(SentEmail))


class ResponsesMock(ResponsesMockServer):
    def response(self, data: dict[str, Any] | str, status: int = 200) -> Response:
        headers = {'Content-Type': 'application/json'}

        if isinstance(data, dict):
            content = json.dumps(data, indent=4, ensure_ascii=False)
        elif isinstance(data, str):
            content = data
        else:
            raise TypeError(f'Invalid data type: {data}')

        return self.Response(text=content, headers=headers, status=status)


@pytest.fixture()
async def mock(event_loop: AbstractEventLoop) -> AsyncGenerator[ResponsesMock, None]:
    async with ResponsesMock(loop=event_loop) as server:
        yield server


@pytest.fixture()
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://testserver') as test_client:
        yield test_client


@pytest.fixture()
async def http_server_url() -> AsyncGenerator[URL, None]:
    router = web.RouteTableDef()

    @router.get('/test')
    @router.post('/test')
    @router.put('/test')
    @router.patch('/test')
    @router.delete('/test')
    async def ok(request: Request) -> Response:
        return web.json_response('ok')

    app = web.Application()
    app.add_routes(router)
    server = TestServer(app)
    await server.start_server()

    yield URL.build(scheme='http', host=server.host, port=server.port)
    await server.close()


@pytest.fixture()
async def sent_emails_repo(db_session: AsyncSession) -> SentEmailRepository:
    return SentEmailRepository(session=db_session)


@pytest.fixture()
def sent_email_service(sent_emails_repo: SentEmailRepository) -> SentEmailService:
    return SentEmailService(sent_emails_repo)


@pytest.fixture(autouse=True)
async def create_service_user(db_session: AsyncSession):
    username, password = API_CREDENTIALS
    hashed_password = hash_password(password)
    new_user = ServiceUser(username=username, password=hashed_password)
    db_session.add(new_user)


@pytest.fixture(autouse=True)
async def setup_data(db_session: AsyncSession) -> None:
    sent_emails = list()
    for _ in range(INIT_CREATE_COUNT):
        sent_email = _generate_fake_sent_email(count=TEST_COUNT)
        sent_emails.append(sent_email)

    db_session.add_all(sent_emails)
    await db_session.commit()
