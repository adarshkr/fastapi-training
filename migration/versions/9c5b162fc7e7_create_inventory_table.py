"""Create inventory table

Revision ID: 9c5b162fc7e7
Revises: 93e3e01d67b6
Create Date: 2024-05-21 12:13:44.901815

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, UTC

# revision identifiers, used by Alembic.
revision = '9c5b162fc7e7'
down_revision = '93e3e01d67b6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "inventory",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("in_stock", sa.Boolean(), nullable=False),
        sa.Column(
            "created_by",
            sa.Integer,
            sa.ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), default=datetime.now(UTC)),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            default=datetime.now(UTC),
            onupdate=datetime.now(UTC),
        ),
    )

    op.create_unique_constraint(
        "inventory_name_created_by_key", "inventory", ["name", "created_by"]
    )
    op.create_index("inventory_idx", "inventory", ["id", "name"])

def downgrade():
    op.drop_constraint("inventory_name_created_by_key", "todo")
    op.drop_index("inventory_idx", "inventory")
    op.drop_table("inventory")