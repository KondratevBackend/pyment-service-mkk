import logging

# Так как у нас распределенный монолит в примере, то используем инстанс консюмер брокера в качестве паблишера
# (такой кейс можно рефакторить в /core, чтобы инстанс брокера не был физически привязан к домену консюмера)
from src.core.brokers import BrokerRabbitMQ
from src.worker.outbox.repository import OutboxWorkerRepository

logger = logging.getLogger(__name__)


class OutboxWorkerService:
    def __init__(self, rabbit: BrokerRabbitMQ, repository: OutboxWorkerRepository):
        self._publisher = rabbit.broker
        self._repository = repository

    async def process(self):
        events = await self._repository.get_unpublished_events()

        for event in events:
            payload = event.get("payload")

            try:
                await self._publisher.publish(
                    message=payload,
                    message_id=payload["idempotency_key"],
                    queue="payments.new",  # todo: Очередь берем из БД
                    exchange="payments",  # todo: Обменник берем из БД
                    persist=True,
                )
                await self._repository.mark_published(outbox_id=event.get("id"))
            except Exception:
                logger.exception("Failed to publish event from outbox")

        # p.s. Так как текущая логики outbox умещается в 5 строк, то вся логика лежит внутри воркера,
        # но если он начнет разрастаться, то можно создать отдельный интерфейс под это всё дело ;)
