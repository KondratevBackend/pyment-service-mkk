from contextlib import asynccontextmanager

import faststream
from faststream.rabbit import RabbitBroker

from src.core.settings import ConsumerSettings


class ConsumerApplication:
    def __init__(
        self,
        config: ConsumerSettings,
    ):
        self._config = config
        self._app = None
        self._rabbit = None

    @property
    def app(self) -> faststream.FastStream:
        if self._app is not None:
            return self._app

        @asynccontextmanager
        async def lifespan():
            yield

        self._app = faststream.FastStream(self.rabbit, lifespan=lifespan)
        self._set_up()

        return self._app

    @property
    def rabbit(self) -> RabbitBroker:
        if self._rabbit is not None:
            return self._rabbit
        self._rabbit = RabbitBroker(str(self._config.broker.dsn))
        return self._rabbit

    def _set_up(self) -> None:
        pass