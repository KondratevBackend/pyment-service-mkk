import fastapi

from src.api.v1.payment.router import PaymentRouter


class V1Router:
    def __init__(self, payment_router: PaymentRouter):
        self._payment_router = payment_router

    @property
    def router(self) -> fastapi.APIRouter:
        router = fastapi.APIRouter(prefix="/v1")
        self._update_routes(router=router)
        return router

    def _update_routes(self, router: fastapi.APIRouter) -> None:
        router.include_router(self._payment_router.router)
