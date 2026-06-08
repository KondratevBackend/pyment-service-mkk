import logging

from taskiq import TaskiqDepends

from src.worker.main import broker, resources
from src.worker.outbox.service import OutboxWorkerService

logger = logging.getLogger(__name__)


def get_service() -> OutboxWorkerService:
    return resources.resolve(OutboxWorkerService)


@broker.task(schedule=[{"interval": 2}])
async def outbox_worker(service: OutboxWorkerService = TaskiqDepends(get_service)):
    logger.info("Outbox job started")
    await service.process()
    logger.info("Outbox job completed")
