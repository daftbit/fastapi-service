from fastapi import Depends
from src.models.organization import Organization
from src.repositories.organization import OrganizationRepository
from src.schemas.organization import OrgnaizationCreateSchema


class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository = Depends()):
        self.organization_repository = organization_repository

    async def create_organization(self, organization: OrgnaizationCreateSchema) -> Organization:
        return await self.organization_repository.create_organization(organization)
