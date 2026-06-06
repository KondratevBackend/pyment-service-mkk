"""
add outbox

Revision ID: 1518d295972e
Revises: 1bc767863f3f  # noqa: UP035
Create Date: 2026-06-06 07:01:12.147973

"""

from typing import Sequence  # noqa: UP035

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1518d295972e"
down_revision: str | None = "1bc767863f3f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "outbox",
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "PROCESSING",
                "PUBLISHED",
                "DEAD_LETTER",
                name="outboxstatustype",
            ),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_outbox")),
    )


def downgrade() -> None:
    op.drop_table("outbox")

    sa.Enum(name="outboxstatustype").drop(op.get_bind(), checkfirst=False)
