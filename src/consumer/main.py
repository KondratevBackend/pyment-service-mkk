import faststream
import punq

from src.consumer import application
from src.consumer.bootstrap import resolve_resources
from src.core.settings import ConsumerSettings

config = ConsumerSettings()
resources: punq.Container = resolve_resources(config=config)
resources.register(
    service=application.ConsumerApplication,
    factory=application.ConsumerApplication,
    scope=punq.Scope.singleton,
    config=config,
)
application: faststream.FastStream = resources.resolve(service_key=application.ConsumerApplication).app
