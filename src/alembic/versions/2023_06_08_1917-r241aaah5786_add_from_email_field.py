"""add_from_email_field

Revision ID: r241aaah5786
Revises: f471hfas6118
Create Date: 2023-06-08 19:17:24.156226

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'r241aaah5786'
down_revision = 'f471hfas6118'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'sent_emails',
        sa.Column(
            'from_email',
            sa.String(length=64),
            server_default='info-mailing@emilegareev.com',
        ),
    )
    op.execute("""UPDATE public.sent_emails SET from_email = '{}'""".format('info-mailing@emilegareev.com'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('from_email', 'from_email')
    # ### end Alembic commands ###
