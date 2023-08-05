"""init

Revision ID: e453dfea7342
Revises:
Create Date: 2023-03-29 10:22:05.613454

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e453dfea7342'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'sent_emails',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('subject', sa.String(length=250), nullable=True),
        sa.Column('recipients', postgresql.ARRAY(sa.String), nullable=False),
        sa.Column('recipient_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_sent_emails_id'), 'sent_emails', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sent_emails_id'), table_name='sent_emails')
    op.drop_table('sent_emails')
    # ### end Alembic commands ###