import fastapi
import punq

from src.api import application
from src.api.bootstrap import resolve_resources
from src.core import settings

config = settings.APISettings()
resources: punq.Container = resolve_resources(config=config)
resources.register(
    service=application.Application,
    factory=application.Application,
    scope=punq.Scope.singleton,
)
app: fastapi.FastAPI = resources.resolve(application.Application).app
