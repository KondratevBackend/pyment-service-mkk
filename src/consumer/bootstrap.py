import punq

from src.consumer.payments.repository import PaymentsRepository
from src.consumer.payments.service import PaymentsService
from src.consumer.payments.subscriptions import PaymentsSubscriptions
from src.core.database import Database
from src.core.settings import ConsumerSettings


def resolve_resources(config: ConsumerSettings) -> punq.Container:
    container = punq.Container()

    container.register(
        service=Database,
        factory=Database,
        scope=punq.Scope.singleton,
        config=config.database,
    )
    container.register(
        service=PaymentsSubscriptions,
        factory=PaymentsSubscriptions,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=PaymentsService,
        factory=PaymentsService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=PaymentsRepository,
        factory=PaymentsRepository,
        scope=punq.Scope.singleton,
    )

    return container
