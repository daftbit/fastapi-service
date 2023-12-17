from fastapi import Body, Depends
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
        response_model=OrganizationSchema,  # Change this to the Pydantic schema
        status_code=201,
        responses={422: {"model": Error, "description": "Unable to process request"}},
    )
    async def create_organization(
        self, organization: OrgnaizationCreateSchema = Body(description="Organization request data")
    ):
        return await self.organization_service.create_organization(organization)
