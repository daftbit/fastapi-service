from uuid import UUID
from fastapi import Depends
from fastapi_pagination import Params, paginate
from fastapi_pagination.bases import AbstractPage
from sqlalchemy import select, and_
from sqlalchemy.exc import StatementError
from sqlalchemy.ext.asyncio import AsyncSession


from src.core.database import Database
from src.core.exceptions.exception import DatabaseException, NotFoundException
from src.models.client import Client
from src.schemas.client import ClientCreateSchema, ClientUpdateSchema


class ClientRepository:
    def __init__(self, session: AsyncSession = Depends(Database.session)):
        self.session = session

    async def create_client(self, organization_id: UUID, client: ClientCreateSchema) -> Client:
        new_client = Client(**client.dict())
        new_client.organization_id = organization_id
        try:
            async with self.session as session:
                async with session.begin():
                    session.add(new_client)
                await session.refresh(new_client)
            return new_client
        except StatementError as exc:
            # TODO: log error
            raise DatabaseException("Internal error", "Unable to create client") from exc

    async def get_clients(self, organization_id: UUID, page_params: Params) -> AbstractPage[Client]:
        try:
            async with self.session as session:
                async with session.begin():
                    query = (
                        select(Client).where(Client.organization_id == organization_id).order_by(Client.modified.desc())
                    )
                    q = await session.execute(query)
            return paginate(q.scalars().unique().all(), page_params)
        except StatementError as exc:
            # TODO: log error
            raise DatabaseException("Internal error", "Unable to retrieve clients") from exc

    async def get_client_by_id(self, organization_id: UUID, client_id: UUID) -> Client:
        try:
            async with self.session as session:
                async with session.begin():
                    query = select(Client).filter(
                        and_(Client.organization_id == organization_id, Client.id == client_id)
                    )
                    q = await session.execute(query)
            existing_client = q.scalars().first()
            if existing_client is None:
                # TODO: log error
                raise NotFoundException("Not found", f"Resource with id {str(client_id)} not found")
            return existing_client
        except StatementError as exc:
            # TODO: log error
            raise DatabaseException("Internal error", "Unable to retrieve client") from exc

    async def patch_client_by_id(self, organization_id: UUID, client_id: UUID, client: ClientUpdateSchema) -> Client:
        try:
            async with self.session as session:
                async with session.begin():
                    query = select(Client).filter(
                        and_(Client.organization_id == organization_id, Client.id == client_id)
                    )
                    q = await session.execute(query)
                    existing_client = q.scalars().first()
                    if existing_client is None:
                        raise NotFoundException("Not found", f"Resource with id {str(client_id)} not found")

                    for column, value in client.dict(exclude_unset=True).items():
                        setattr(existing_client, column, value)
        except StatementError as exc:
            # TODO: log error
            raise DatabaseException("Internal error", "Unable to update client") from exc
