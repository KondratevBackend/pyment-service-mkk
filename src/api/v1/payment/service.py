import fastapi
from sqlalchemy.exc import IntegrityError

from src.api.v1.payment import schemes
from src.api.v1.payment.repository import PaymentRepository
from src.core.database.models import Payment


class PaymentService:
    def __init__(self, repository: PaymentRepository):
        self._repository = repository

    async def get_payment(self, payment_id: int) -> schemes.PaymentResponse:
        payment = await self._repository.get_payment(payment_id=payment_id)

        if payment is None:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="Payment not found",
            )

        return schemes.PaymentResponse.model_validate(payment, from_attributes=True)

    async def create_payment(
        self,
        payload: schemes.CreatePaymentRequest,
        idempotency_key: str,
    ) -> schemes.CreatePaymentResponse:
        try:
            payment: Payment = await self._repository.insert_payment(payload=payload, idempotency_key=idempotency_key)
        except IntegrityError:  # На продакшене такую ошибку лучше закастомить, чтобы логика ниже сразу объяснялась
            # Можно кинуть и 409. Но при идемпотентности, как правило, не кидают, поэтому запрашиваем тот же инстанс
            payment: Payment = await self._repository.get_payment_by_idempotency_key(idempotency_key=idempotency_key)

        return schemes.CreatePaymentResponse.model_validate(payment, from_attributes=True)
