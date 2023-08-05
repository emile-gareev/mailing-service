from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class BasicRepository(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    @abstractmethod
    async def get_all(self, page: int, limit: int):
        ...

    @abstractmethod
    async def get_by_id(self, entry_id: int):
        ...

    async def save(self) -> None:
        await self._session.commit()
