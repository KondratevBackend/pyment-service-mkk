import punq

from src.core.settings import WorkerSettings
from src.core.database import Database


def resolve_resources(config: WorkerSettings) -> punq.Container:
    container = punq.Container()

    container.register(
        service=Database,
        factory=Database,
        scope=punq.Scope.singleton,
        config=config.database,
    )

    return container
