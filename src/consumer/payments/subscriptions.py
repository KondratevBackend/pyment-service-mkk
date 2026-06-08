from faststream import Context
from faststream.rabbit import QueueType, RabbitBroker, RabbitExchange, RabbitMessage, RabbitQueue, RabbitRouter

from src.consumer.payments import exchanges
from src.consumer.payments.schemes import Payment
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
        @router.subscriber(queue=RabbitQueue(name="new", durable=True), exchange=exchanges.payment_exchange)
        async def payments_new_handler(payment: Payment, msg: RabbitMessage, broker: RabbitBroker = Context()):
            await self._service.process_payment(payment=payment, msg=msg, broker=broker)

    @staticmethod
    async def declare(broker: RabbitBroker) -> None:
        # делей реализован через DLX + TTL с целью показать работу с exchanges, но в реальности можно взять
        # rabbitmq_delayed_message_exchange или реализовать отдельный интерфейс для retry через DLX TTL
        retry_1 = await broker.declare_queue(
            RabbitQueue(
                name="payments.retry.1",
                durable=True,
                arguments={
                    "x-message-ttl": 5 * 1000,
                    "x-dead-letter-exchange": exchanges.payment_exchange.name,
                    "x-dead-letter-routing-key": "payments.new",
                },
            ),
        )
        await retry_1.bind(exchanges.payment_exchange.name)

        retry_2 = await broker.declare_queue(
            RabbitQueue(
                name="payments.retry.2",
                durable=True,
                arguments={
                    "x-message-ttl": 25 * 1000,
                    "x-dead-letter-exchange": exchanges.payment_exchange.name,
                    "x-dead-letter-routing-key": "payments.new",
                },
            ),
        )
        await retry_2.bind(exchanges.payment_exchange.name)

        retry_3 = await broker.declare_queue(
            RabbitQueue(
                name="payments.retry.3",
                durable=True,
                arguments={
                    "x-message-ttl": 125 * 1000,
                    "x-dead-letter-exchange": exchanges.payment_exchange.name,
                    "x-dead-letter-routing-key": "payments.new",
                },
            ),
        )
        await retry_3.bind(exchanges.payment_exchange.name)
