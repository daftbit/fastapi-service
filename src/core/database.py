import json
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.core.settings import get_config

Base = declarative_base()


class Database:
    """Singleton databsase class to provide application context to a connection."""

    __engine: AsyncEngine = None
    __session_maker: sessionmaker = None

    @classmethod
    async def session(cls) -> AsyncSession:
        session: AsyncSession = cls.__session_maker()
        try:
            yield session
        except Exception as exc:
            await session.rollback()
            raise
        finally:
            await session.close()

    @classmethod
    def get_engine(cls):
        if Database.__engine is None:
            Database.__engine = create_async_engine(
                cls.get_database_url(),
                echo=False,  # show logging of statements and sql execution
                pool_pre_ping=True,  # enable the connection pool
                future=True,
                json_serializer=json.dumps,
                json_deserializer=json.loads,
                max_overflow=10,  # number of connections within the connection pool
                pool_size=10,
                echo_pool=False,  # show logging for connection pool
            )
        return cls.__engine

    @classmethod
    async def open_database_connection(cls):
        if Database.__engine is None:
            Database.__engine = create_async_engine(
                cls.get_database_url(),
                echo=False,  # show logging of statements and sql execution
                pool_pre_ping=True,  # enable the connection pool
                future=True,
                json_serializer=json.dumps,
                json_deserializer=json.loads,
                max_overflow=10,  # number of connections within the connection pool
                pool_size=10,
                echo_pool=False,  # show logging for connection pool
            )
        if Database.__session_maker is None:
            Database.__session_maker = sessionmaker(bind=cls.__engine, expire_on_commit=False, class_=AsyncSession)

    @classmethod
    async def close_database_connection(cls):
        if Database.__engine is not None:
            await Database.__engine.dispose()

    @classmethod
    def get_database_url(cls) -> str:
        return get_config()["Database"]["url"]
