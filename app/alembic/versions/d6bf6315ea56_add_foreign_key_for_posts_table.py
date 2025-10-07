"""add foreign key for posts table

Revision ID: d6bf6315ea56
Revises: fadd3c54d515
Create Date: 2025-10-07 09:59:13.955458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6bf6315ea56'
down_revision: Union[str, Sequence[str], None] = 'fadd3c54d515'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1️⃣ Add the column first
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    # add foreign key to posts.owner_id referencing users.id
    op.create_foreign_key(
        "fk_posts_owner_id_users",  # constraint name
        "posts",                    # source table
        "users",                    # target table
        ["owner_id"],               # source columns
        ["id"],                     # target columns
        ondelete="CASCADE"          # optional
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_posts_owner_id_users",
        "posts",
        type_="foreignkey"
    )
    # 2️⃣ Drop the column
    op.drop_column("posts", "owner_id")
    pass
