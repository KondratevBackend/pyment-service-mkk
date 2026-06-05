import fastapi

from src.api.v1.payment import schemes
from src.api.v1.payment.service import PaymentService


class PaymentRouter:
    def __init__(self, service: PaymentService):
        self._service = service

    @property
    def router(self) -> fastapi.APIRouter:
        router = fastapi.APIRouter(prefix="/payments", tags=["Payments"])
        self.include_routes(router=router)
        return router

    def include_routes(self, router: fastapi.APIRouter) -> None:
        @router.get(
            path="/{payment_id}",
            description="Get details info of payment by id",
            status_code=fastapi.status.HTTP_200_OK,
            response_model=schemes.PaymentResponse,
        )
        async def get_payment(payment_id: int) -> fastapi.Response:
            return await self._service.get_payment(payment_id=payment_id)

        @router.post(
            path="",
            description="Create payment",
            status_code=fastapi.status.HTTP_202_ACCEPTED,
            response_model=schemes.CreatePaymentResponse,
        )
        async def create_payment(
            payload: schemes.CreatePaymentRequest,
            idempotency_key: str = fastapi.Header(..., alias="Idempotency-Key"),
        ) -> fastapi.Response:
            return await self._service.create_payment(
                payload=payload, idempotency_key=idempotency_key
            )
