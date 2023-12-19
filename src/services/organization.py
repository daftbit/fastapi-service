from uuid import UUID
from fastapi import Depends
from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from src.models.organization import Organization
from src.repositories.organization import OrganizationRepository
from src.schemas.organization import OrganizationSchema, OrganizationCreateSchema, OrganizationUpdateSchema


class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository = Depends()):
        self.organization_repository = organization_repository

    async def create_organization(self, organization: OrganizationCreateSchema) -> Organization:
        return await self.organization_repository.create_organization(organization)

    async def get_organizations(self, page_params: Params, user_id: UUID) -> AbstractPage[OrganizationSchema]:
        return await self.organization_repository.get_organizations(page_params, user_id)

    async def get_organization_by_id(self, organization_id: UUID, user_id: UUID) -> OrganizationSchema:
        return await self.organization_repository.get_organization_by_id(organization_id, user_id)

    async def patch_organization_by_id(
        self, organization_id: UUID, organization: OrganizationUpdateSchema, user_id: UUID
    ) -> Organization:
        return await self.organization_repository.patch_organization_by_id(organization_id, organization, user_id)
