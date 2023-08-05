from app.db.connection import Session
from app.db.models import ServiceUser
from app.utils.security import hash_password


async def create_service_user(username: str, password: str):
    """Create new service user."""
    if not (username and password):
        raise Exception('No username or password provided or both. Try again.')

    hashed_password = hash_password(password)
    new_user = ServiceUser(username=username, password=hashed_password)

    async with Session() as session:
        session.add(new_user)
        await session.commit()
