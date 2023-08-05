import sqlalchemy as sa
import typing as t
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ORJSONModel, ServiceUser


class ServiceUserSchema(ORJSONModel):
    class Config:
        use_enum_values = True
        orm_mode = True

    id: int  # noqa: A003, VNE003
    username: str
    password: str
    email: t.Optional[str]
    is_active: bool


class ServiceUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def get_user_by_username(self, username: str) -> t.Optional[ServiceUserSchema]:
        query = sa.select(ServiceUser).where(ServiceUser.username == username)
        result = await self._session.scalars(query)
        user = result.first()

        if user:
            return ServiceUserSchema.from_orm(user)

        return None

    async def save(self) -> None:
        await self._session.commit()
