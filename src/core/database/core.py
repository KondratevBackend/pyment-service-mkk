import re
from collections.abc import AsyncGenerator

import sqlalchemy
from sqlalchemy import inspection
from sqlalchemy.ext import asyncio
from sqlalchemy.orm import declarative_base, declared_attr

from src.core import settings


class Database:
    def __init__(self, config: settings.DatabaseSettings):
        self._db_dsn = config.dsn.unicode_string().replace(
            "postgresql", "postgresql+asyncpg"
        )
        self._engine = asyncio.create_async_engine(
            self._db_dsn,
            echo=True,
            pool_size=config.engine_pool_size,
            max_overflow=config.engine_max_overflow,
            pool_timeout=config.engine_pool_timeout,
            pool_pre_ping=config.engine_pool_ping,
        )
        self._session_local = asyncio.async_sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    async def get_session(self) -> AsyncGenerator[asyncio.AsyncSession]:
        async with self._session_local() as session:
            yield session

    @property
    def engine(self):
        return self._engine

    async def shutdown(self):
        await self._engine.dispose()


class CustomBase:
    __table__: sqlalchemy.Table

    @staticmethod
    def resolve_table_name(name: str) -> str:
        """Resolves table names to their mapped names"""
        names = re.split("(?=[A-Z])", name)
        return "_".join([x.lower() for x in names if x])

    @staticmethod
    def is_composite_key(ids) -> bool:
        return len(ids) > 1

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return cls.resolve_table_name(cls.__name__)

    @classmethod
    def get_columns_names(cls) -> tuple:
        return tuple(cls.__table__.columns.keys())

    @property
    def _id_str(self) -> str:
        ids: tuple = inspection.inspect(self).identity
        if ids:
            return (
                "-".join([str(x) for x in ids])
                if self.is_composite_key(ids)
                else str(ids[0])
            )
        return "None"

    def __repr__(self):
        id_str = ("#" + self._id_str) if self._id_str else ""  # get id '#123'
        return f"<{self.__class__.__name__} {id_str}>"


Base = declarative_base(
    cls=CustomBase,
    metadata=sqlalchemy.MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    ),
)
