import logging

from faststream.rabbit import RabbitBroker

from src.core import settings

logger = logging.getLogger(__name__)


class BrokerRabbitMQ:
    def __init__(self, config: settings.BrokerSettings):
        self._config = config
        self._broker: RabbitBroker = RabbitBroker(self._config.dsn.unicode_string())

    @property
    def broker(self) -> RabbitBroker:
        # Так как нам сейчас не надо контролировать все сценарии поведения (начиная от создания/выключения,
        # заканчивая публикацией/кейсами), то я просто отдаю брокер наружу.
        # Ещё как хороший кейс, можно отдавать инстанс брокера под видам пула готовых коннектов
        return self._broker
