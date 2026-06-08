import sqlalchemy

from src.core.database import Database
from src.core.database.models import Payment
from src.core.database.models.payment import PaymentStatusType


class PaymentsRepository:
    def __init__(self, database: Database):
        self._database = database

    async def exists_duplicate_payment_by_idempotency_key(self, idempotency_key: str) -> bool:
        query = sqlalchemy.select(
            sqlalchemy.exists().where(
                Payment.idempotency_key == idempotency_key,
                Payment.status != PaymentStatusType.PENDING,
            )
        )

        async for session in self._database.get_session():
            result = await session.execute(query)

        return result.scalar_one()

    async def update_payment_status(self, payment_id: int, status: PaymentStatusType) -> None:
        query = sqlalchemy.update(Payment).where(Payment.id == payment_id).values(status=status)

        async for session in self._database.get_session():
            await session.execute(query)
            await session.commit()
