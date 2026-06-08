import logging

from faststream.rabbit import RabbitBroker
from taskiq import TaskiqEvents, TaskiqScheduler, TaskiqState
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker, Queue, QueueType, Exchange
from aio_pika import ExchangeType

from src.core.brokers import BrokerRabbitMQ
from src.core.settings import WorkerSettings

logger = logging.getLogger(__name__)


class WorkerApplication:
    def __init__(self, rabbit: BrokerRabbitMQ, config: WorkerSettings):
        self._faststream_broker: RabbitBroker = rabbit.broker
        self._config = config
        self._broker = None
        self._scheduler = None

    @property
    def broker(self) -> AioPikaBroker:
        if self._broker is not None:
            return self._broker

        _broker = AioPikaBroker(
            url=self._config.broker.dsn.unicode_string(),
            exchange=Exchange(
                name="taskiq_exchange",
                type=ExchangeType.TOPIC,
                declare=True,
                durable=True,
                auto_delete=False,
            ),
            task_queues=[
                Queue(
                    name="taskiq_queue",
                    type=QueueType.CLASSIC,
                    declare=True,
                    durable=True,
                    max_priority=10,
                    routing_key="taskiq_queue",
                )
            ]
        )
        self._broker = _broker

        self._register_events(broker=_broker)

        return _broker

    @property
    def scheduler(self) -> TaskiqScheduler:
        if self._scheduler is not None:
            return self._scheduler

        _scheduler = TaskiqScheduler(
            broker=self.broker,
            sources=[LabelScheduleSource(self.broker)],
        )
        self._scheduler = _scheduler

        return _scheduler

    def _register_events(self, broker) -> None:
        @broker.on_event(TaskiqEvents.WORKER_STARTUP)
        async def startup(state: TaskiqState) -> None:
            await self._faststream_broker.start()
            logger.info("Worker startup")

        @broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
        async def shutdown(state: TaskiqState) -> None:
            await self._faststream_broker.stop()
            logger.info("Worker shutdown")
