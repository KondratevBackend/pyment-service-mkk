import sqlalchemy

from src.api.v1.payment import schemes
from src.core.database import Database
from src.core.database.models import Payment
from src.core.database.models.payment import PaymentStatusType


class PaymentRepository:
    def __init__(self, database: Database):
        self._database = database

    async def exists_payment(self, idempotency_key: str) -> bool:
        query = sqlalchemy.select(sqlalchemy.exists().where(Payment.idempotency_key == idempotency_key))

        async for session in self._database.get_session():
            result = await session.execute(query)

        return result.scalar()

    async def get_payment_by_idempotency_key(self, idempotency_key: str) -> Payment:
        # Для простоты примера взял фулл объект платежа
        query = (sqlalchemy.select(Payment).where(Payment.idempotency_key == idempotency_key))

        async for session in self._database.get_session():
            result = await session.execute(query)

        return result.scalar_one()

    async def insert_payment(self, payload: schemes.CreatePaymentRequest, idempotency_key: str) -> Payment:
        instance = Payment(
            sum=payload.sum,
            currency=payload.currency,
            description=payload.description,
            meta_data=payload.meta_data,
            webhook_url=str(payload.webhook_url),
            idempotency_key=idempotency_key,
            status=PaymentStatusType.PENDING,
        )

        async for session in self._database.get_session():
            session.add(instance)
            await session.commit()

        return instance
