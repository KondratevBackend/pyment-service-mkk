import punq
from taskiq import TaskiqScheduler
from taskiq_aio_pika import AioPikaBroker

from src.core.settings import WorkerSettings
from src.worker.application import WorkerApplication
from src.worker.bootstrap import resolve_resources

config = WorkerSettings()
resources: punq.Container = resolve_resources(config=config)
resources.register(service=WorkerApplication, factory=WorkerApplication, scope=punq.Scope.singleton, config=config)
application: WorkerApplication = resources.resolve(service_key=WorkerApplication)
broker: AioPikaBroker = application.broker
scheduler: TaskiqScheduler = application.scheduler
