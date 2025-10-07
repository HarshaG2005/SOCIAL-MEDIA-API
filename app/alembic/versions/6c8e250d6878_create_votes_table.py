"""create votes table

Revision ID: 6c8e250d6878
Revises: d6bf6315ea56
Create Date: 2025-10-07 10:06:17.929692

"""
from typing import Sequence, Union
from sqlalchemy import ForeignKey
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c8e250d6878'
down_revision: Union[str, Sequence[str], None] = 'd6bf6315ea56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'votes',
        sa.Column('post_id',sa.Integer,ForeignKey('posts.id',ondelete='CASCADE'),primary_key=True,nullable=False),
        sa.Column('user_id',sa.Integer,sa.ForeignKey('users.id',ondelete='CASCADE'),primary_key=True,nullable=False),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('votes')
    pass
