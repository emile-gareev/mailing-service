# type: ignore
from __future__ import annotations

import logging
from typing import Callable

logger = logging.getLogger(__name__)


async def _get_session():
    try:
        # cita
        from app.async_db import db_session

        return db_session  # pragma: no cover
    except ImportError:
        logger.debug("[Healthcheck] Import CITA DB session was failed")

    try:
        from app.db.postgres.connections import get_session

        return await get_session()  # pragma: no cover
    except ImportError:
        logger.debug("[Healthcheck] Import generic DB session was failed")


async def get_postgres_issues() -> None | str:
    """
    Can be useful to check Postgres / asyncpg connections heath.
    check_tortoise is a temporary solution, must be wipe-out after migration to Alchemy
    (mark for ancestors: 02.02.2023)
    Return exception string if check goes wrong
    """
    checker: Callable[[], Exception | None] | None = await get_check_func()

    if not checker:
        logger.error("[Healthcheck] Cannot get Postgres health check function")
        return None

    try:
        await checker()
    except Exception as err:
        return str(err)


async def get_check_func() -> Callable | None:
    try:  # pragma: no cover
        from tortoise import Tortoise

        async def check_tortoise() -> None:
            try:
                await Tortoise.get_connection("healthcheck").execute_query("SELECT 1")
            except Exception as err:
                raise err

        return check_tortoise
    except ImportError:
        logger.debug("[Healthcheck] Tortoise not imported, skipping")
        pass
    try:  # pragma: no cover
        import sqlalchemy  # noqa F401

        alchemy_session = await _get_session()

        async def check_alchemy() -> None:
            try:
                async with alchemy_session() as _session:
                    await _session.execute("SELECT 1")
            except Exception as err:
                raise err

        return check_alchemy
    except ImportError:
        logger.debug("[Healthcheck] Alchemy not imported, skipping")
        pass
