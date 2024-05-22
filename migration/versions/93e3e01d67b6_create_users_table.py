"""Create users table

Revision ID: 93e3e01d67b6
Revises:
Create Date: 2024-05-21 11:52:13.679515

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, UTC


# revision identifiers, used by Alembic.
revision = '93e3e01d67b6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(), unique=True, nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), default=datetime.now(UTC)),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            default=datetime.now(UTC),
            onupdate=datetime.now(UTC),
        ),
    )
    op.create_index("user_idx", "user", ["id", "username"])


def downgrade():
    op.drop_index("user_idx", "user")
    op.drop_table("user")
