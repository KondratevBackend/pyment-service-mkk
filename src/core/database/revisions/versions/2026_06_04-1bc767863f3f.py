"""
add payment

Revision ID: 1bc767863f3f
Revises:   # noqa: UP035
Create Date: 2026-06-04 23:57:29.829810

"""

from typing import Sequence  # noqa: UP035

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1bc767863f3f"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "payment",
        sa.Column("sum", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "currency",
            sa.Enum("RUB", "USD", "EUR", name="currencytype"),
            nullable=False,
        ),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("meta_data", sa.JSON(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING", "SUCCEEDED", "FAILED", name="paymentstatustype"
            ),
            nullable=False,
        ),
        sa.Column("webhook_url", sa.String(length=256), nullable=True),
        sa.Column("idempotency_key", sa.Uuid(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_payment")),
    )
    op.create_index(
        op.f("ix_payment_idempotency_key"),
        "payment",
        ["idempotency_key"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_payment_idempotency_key"), table_name="payment")
    op.drop_table("payment")

    sa.Enum(name="paymentstatustype").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="currencytype").drop(op.get_bind(), checkfirst=False)
