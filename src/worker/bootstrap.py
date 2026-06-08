import punq

from src.core.brokers import BrokerRabbitMQ
from src.core.settings import WorkerSettings
from src.core.database import Database
from src.worker.outbox.repository import OutboxWorkerRepository
from src.worker.outbox.service import OutboxWorkerService


def resolve_resources(config: WorkerSettings) -> punq.Container:
    container = punq.Container()

    container.register(
        service=Database,
        factory=Database,
        scope=punq.Scope.singleton,
        config=config.database,
    )
    container.register(
        service=BrokerRabbitMQ,
        factory=BrokerRabbitMQ,
        scope=punq.Scope.singleton,
        config=config.broker,
    )
    container.register(
        service=OutboxWorkerService,
        factory=OutboxWorkerService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=OutboxWorkerRepository,
        factory=OutboxWorkerRepository,
        scope=punq.Scope.singleton,
    )

    return container
