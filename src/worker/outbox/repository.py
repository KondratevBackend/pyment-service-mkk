import sqlalchemy

from src.core.database import Database
from src.core.database.models.outbox import Outbox, OutboxStatusType


class OutboxWorkerRepository:
    def __init__(self, database: Database):
        self._database = database

    async def get_unpublished_events(self) -> list[dict]:
        query = sqlalchemy.select(Outbox.id, Outbox.payload).where(Outbox.status == OutboxStatusType.PENDING)

        async for session in self._database.get_session():
            result = await session.execute(query)

        return result.mappings().all()

    async def mark_published(self, outbox_id: int) -> None:
        query = sqlalchemy.update(Outbox).where(Outbox.id == outbox_id).values(status=OutboxStatusType.PUBLISHED)

        async for session in self._database.get_session():
            await session.execute(query)
            await session.commit()
