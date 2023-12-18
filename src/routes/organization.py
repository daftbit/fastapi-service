from uuid import UUID
from fastapi import Body, Depends, Query
from fastapi_pagination import Page, Params
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from src.schemas.organization import OrganizationSchema, OrgnaizationCreateSchema

from src.services.organization import OrganizationService
from src.schemas.error import Error

organization = InferringRouter()


@cbv(organization)
class Organization:
    def __init__(self, organization_service: OrganizationService = Depends()):
        self.organization_service = organization_service

    @organization.post(
        "/organization",
        tags=["Organization"],
        response_model=OrganizationSchema,
        status_code=201,
        responses={422: {"model": Error, "description": "Unable to process request"}},
    )
    async def create_organization(
        self, organization: OrgnaizationCreateSchema = Body(description="Organization request data")
    ):
        return await self.organization_service.create_organization(organization)
    
    
    @organization.get(
        "/organization",
        tags=["Organization"],
        response_model=Page[OrganizationSchema],
        responses={422: {"model": Error, "description": "Unable to process request"}},
    )
    async def get_organizations(self, page_params: Params = Depends(), user_id: UUID = Query()):
        return await self.organization_service.get_organizations(page_params, user_id)
