import punq

from src.api.health_checks.router import HealthChecksRouter
from src.api.v1.payment.repository import PaymentRepository
from src.api.v1.payment.router import PaymentRouter
from src.api.v1.payment.service import PaymentService
from src.api.v1.router import V1Router
from src.core.database import Database
from src.core.settings import APISettings


def resolve_resources(config: APISettings) -> punq.Container:
    container = punq.Container()

    container.register(
        service=Database,
        factory=Database,
        scope=punq.Scope.singleton,
        config=config.database,
    )
    container.register(
        service=HealthChecksRouter,
        factory=HealthChecksRouter,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=V1Router,
        factory=V1Router,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=PaymentRouter,
        factory=PaymentRouter,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=PaymentService,
        factory=PaymentService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=PaymentRepository,
        factory=PaymentRepository,
        scope=punq.Scope.singleton,
    )

    return container
