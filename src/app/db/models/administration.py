import sqlalchemy as sa

from app.db.models.base import Base


class ServiceUser(Base):
    """Technical user for internal API connection."""

    __tablename__ = 'service_users'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True, index=True)  # noqa: A003, VNE003
    username = sa.Column(sa.String(50), unique=True, nullable=False)
    email = sa.Column(sa.String(100))
    password = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
