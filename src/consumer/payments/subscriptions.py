from faststream.rabbit import RabbitQueue, RabbitRouter

from src.consumer.payments import exchanges
from src.consumer.payments.service import PaymentsService
from src.core import consts


class PaymentsSubscriptions:
    def __init__(self, service: PaymentsService):
        self._service = service

    @property
    def router(self) -> RabbitRouter:
        router = RabbitRouter(prefix="payments.")
        self._include_routes(router=router)
        return router

    def _include_routes(self, router: RabbitRouter) -> None:
        @router.subscriber(
            queue=RabbitQueue(
                name="new",
                durable=True,
                arguments={
                    "x-dead-letter-exchange": consts.DEAD_LETTER_EXCHANGE,
                    "x-dead-letter-routing-key": consts.DEAD_LETTER_ROUTING_KEY,
                },
            ),
            exchange=exchanges.payment_exchange,
        )
        async def payments_new_handler():
            await self._service.process_payment()
