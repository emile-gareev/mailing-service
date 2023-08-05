import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimeMixin:
    updated_at = sa.Column(
        sa.DateTime(timezone=False),
        onupdate=datetime.utcnow,
        default=datetime.utcnow,
        server_default=sa.sql.func.now(),
        nullable=False,
    )
    created_at = sa.Column(
        sa.DateTime(timezone=False),
        default=datetime.utcnow,
        server_default=sa.sql.func.now(),
        nullable=False,
    )
