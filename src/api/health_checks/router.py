import fastapi
import sqlalchemy
from sqlalchemy import exc as sqlalchemy_exc

from src.core import database


class HealthChecksRouter:
    def __init__(self, db: database.Database):
        self._db = db

    @property
    def router(self) -> fastapi.APIRouter:
        router = fastapi.APIRouter(prefix="/health", tags=["Health Checks API"])
        self.include_routes(router=router)
        return router

    def include_routes(self, router: fastapi.APIRouter) -> None:
        @router.get("/ping")
        async def get_ping():
            return "pong"

        @router.get(
            "/ready",
            responses={
                500: {"description": "Database connection error"},
            },
        )
        async def get_ready():
            try:
                async for session in self._db.get_session():
                    await session.execute(sqlalchemy.text("SELECT version()"))
                return "ready"
            except sqlalchemy_exc.SQLAlchemyError as e:
                raise fastapi.HTTPException(
                    status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database connection error",
                ) from e
