import logging

import faststream
from faststream.rabbit import RabbitExchange, RabbitQueue, RabbitBroker

from src.consumer.payments.subscriptions import PaymentsSubscriptions
from src.core import consts, brokers
from src.core.settings import ConsumerSettings

logger = logging.getLogger(__name__)


class ConsumerApplication:
    def __init__(
        self,
        payment_subscriptions: PaymentsSubscriptions,
        rabbit: brokers.BrokerRabbitMQ,
        config: ConsumerSettings,
    ):
        self._broker: RabbitBroker = rabbit.broker
        self._payment_subscriptions = payment_subscriptions
        self._config = config
        self._app = None
        self._rabbit = None

    @property
    def app(self) -> faststream.FastStream:
        if self._app is not None:
            return self._app

        self._app = faststream.FastStream(
            self._broker,
            on_startup=[self.startup_hook],
            after_startup=[self.after_startup_hook],
            after_shutdown=[self.after_shutdown_hook],
            on_shutdown=[self.shutdown_hook],
        ).as_asgi(asyncapi_path="/docs/asyncapi")
        self._set_up()

        return self._app

    def _set_up(self) -> None:
        self._broker.include_router(self._payment_subscriptions.router)

    async def startup_hook(self):
        logger.info("on_startup called")

    async def after_startup_hook(self):
        logger.info("after_startup called")
        await self._declare_dead_letter()
        await self._payment_subscriptions.declare(broker=self._broker)

    async def shutdown_hook(self):
        logger.info("on_shutdown called")

    async def after_shutdown_hook(self):
        logger.info("after_shutdown called")

    async def _declare_dead_letter(self):
        # Для простоты примера я не разбивал exchanges на доменные области
        dead_letter_exchange = await self._broker.declare_exchange(
            RabbitExchange(
                name=consts.DEAD_LETTER_EXCHANGE,
                durable=True,
            )
        )
        dead_letter_queue = await self._broker.declare_queue(
            RabbitQueue(
                name=consts.DEAD_LETTER_QUEUE,
                durable=True,
            )
        )
        await dead_letter_queue.bind(dead_letter_exchange, routing_key=consts.DEAD_LETTER_ROUTING_KEY)
