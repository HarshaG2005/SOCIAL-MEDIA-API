"""Add Posts table

Revision ID: 1c8a4a6ac5fa
Revises: 
Create Date: 2025-10-07 08:35:45.646297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '1c8a4a6ac5fa'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('published', sa.Boolean, server_default=sa.true()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")),
        #sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
