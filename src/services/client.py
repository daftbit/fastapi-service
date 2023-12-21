from uuid import UUID
from fastapi import Depends
from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage

from src.models.client import Client
from src.repositories.client import ClientRepository
from src.repositories.organization import OrganizationRepository
from src.schemas.client import ClientCreateSchema, ClientUpdateSchema


class ClientService:
    def __init__(
        self,
        organization_repository: OrganizationRepository = Depends(),
        client_repository: ClientRepository = Depends(),
    ):
        self.organization_repository = organization_repository
        self.client_repository = client_repository

    async def create_client(self, organization_id: UUID, client: ClientCreateSchema, user_id: UUID) -> Client:
        await self.organization_repository.get_organization_by_id(organization_id, user_id)
        return await self.client_repository.create_client(organization_id, client)

    async def get_clients(self, organization_id: UUID, page_params: Params, user_id: UUID) -> AbstractPage[Client]:
        await self.organization_repository.get_organization_by_id(organization_id, user_id)
        return await self.client_repository.get_clients(organization_id, page_params)

    async def get_client_by_id(self, organization_id: UUID, client_id: UUID, user_id: UUID) -> Client:
        await self.organization_repository.get_organization_by_id(organization_id, user_id)
        return await self.client_repository.get_client_by_id(organization_id, client_id)

    async def patch_client_by_id(
        self, organization_id: UUID, client_id: UUID, client: ClientUpdateSchema, user_id: UUID
    ) -> Client:
        await self.organization_repository.get_organization_by_id(organization_id, user_id)
        return await self.client_repository.patch_client_by_id(organization_id, client_id, client)
