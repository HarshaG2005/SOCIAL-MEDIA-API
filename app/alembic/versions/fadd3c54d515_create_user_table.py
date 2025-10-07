"""create user table

Revision ID: fadd3c54d515
Revises: 1c8a4a6ac5fa
Create Date: 2025-10-07 09:45:41.634155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'fadd3c54d515'
down_revision: Union[str, Sequence[str], None] = '1c8a4a6ac5fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id',sa.Integer,primary_key=True,nullable=False),
        sa.Column('email',sa.String,nullable=False,unique=True),
        sa.Column('password',sa.String,nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
