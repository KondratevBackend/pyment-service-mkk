import enum
import uuid
from decimal import Decimal

from sqlalchemy import JSON, Enum, Numeric, String, Uuid, orm

from src.core.database import Base, mixins


class CurrencyType(enum.StrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class PaymentStatusType(enum.StrEnum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class Payment(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    sum: orm.Mapped[Decimal] = orm.mapped_column(Numeric(precision=10, scale=2), nullable=False)
    currency: orm.Mapped[CurrencyType] = orm.mapped_column(Enum(CurrencyType), nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(String, nullable=True)
    meta_data: orm.Mapped[JSON] = orm.mapped_column(type_=JSON, nullable=True)
    status: orm.Mapped[PaymentStatusType] = orm.mapped_column(Enum(PaymentStatusType), nullable=False)
    webhook_url: orm.Mapped[str] = orm.mapped_column(String(length=256), nullable=True)
    idempotency_key: orm.Mapped[uuid.UUID] = orm.mapped_column(
        Uuid,
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4,
    )
