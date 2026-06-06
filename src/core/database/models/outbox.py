import enum

from sqlalchemy import orm, JSON, Enum

from src.core.database import Base, mixins


class OutboxStatusType(enum.StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    PUBLISHED = "published"
    DEAD_LETTER = "dead_letter"


class Outbox(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    payload: orm.Mapped[JSON] = orm.mapped_column(type_=JSON, nullable=False)
    status: orm.Mapped[OutboxStatusType] = orm.mapped_column(
        Enum(OutboxStatusType),
        nullable=False,
        default=OutboxStatusType.PENDING,
    )

    # Реализовал простой случай, но можно добавить ещё пару полезных полей:
    # 1. Количество попыток (ретраев)
    # 2. Следующее время ретрая (ретраи делаем с инкрементом)
    # 3. Queue
    # 4. Exchange
