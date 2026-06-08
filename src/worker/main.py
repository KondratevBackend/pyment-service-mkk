import punq
from taskiq import TaskiqScheduler
from taskiq_aio_pika import AioPikaBroker

from src.core.settings import WorkerSettings
from src.worker.application import WorkerApplication
from src.worker.bootstrap import resolve_resources

config = WorkerSettings()
container: punq.Container = resolve_resources(config=config)
container.register(service=WorkerApplication, factory=WorkerApplication, scope=punq.Scope.singleton, config=config)
application: WorkerApplication = container.resolve(service_key=WorkerApplication)
broker: AioPikaBroker = application.broker
scheduler: TaskiqScheduler = application.scheduler
