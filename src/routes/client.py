from pathlib import Path
from uuid import UUID
from fastapi import Body, Depends, Query
from fastapi_pagination import Page, Params
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from src.schemas.client import ClientCreateSchema, ClientSchema, ClientUpdateSchema
from src.schemas.error import Error

from src.services.client import ClientService

client = InferringRouter()


@cbv(client)
class Client:
    # TODO add auth with JWT
    # Remove the need to have user_id as query param once IAM is implemented
    def __init__(self, client_service: ClientService = Depends()):
        self.client_service = client_service

    @client.post(
        "/organization/{organization_id}/client",
        tags=["Client"],
        response_model=ClientSchema,
        status_code=201,
        responses={
            422: {"model": Error, "description": "Unable to process request"},
            404: {"model": Error, "description": "Resource not found"},
            500: {"model": Error, "description": "Server error"},
        },
    )
    async def create_client(
        self,
        organization_id: UUID = Path(description="Identifier for the organization"),
        client: ClientCreateSchema = Body(description="Client request data"),
        user_id: UUID = Query(),
    ):
        return await self.client_service.create_client(organization_id, client, user_id)

    @client.get(
        "/organization/{organization_id}/client",
        tags=["Client"],
        response_model=Page[ClientSchema],
        responses={
            422: {"model": Error, "description": "Unable to process request"},
            404: {"model": Error, "description": "Resource not found"},
            500: {"model": Error, "description": "Server error"},
        },
    )
    async def get_clients(
        self,
        organization_id: UUID = Path(description="Identifier for the organization"),
        page_params: Params = Depends(),
        user_id: UUID = Query(),
    ):
        return await self.client_service.get_clients(organization_id, page_params, user_id)

    @client.get(
        "/organization/{organization_id}/client/{client_id}",
        tags=["Client"],
        response_model=ClientSchema,
        responses={
            422: {"model": Error, "description": "Unable to process request"},
            404: {"model": Error, "description": "Resource not found"},
            500: {"model": Error, "description": "Server error"},
        },
    )
    async def get_client_by_id(
        self,
        organization_id: UUID = Path(description="Identifier for the organization"),
        client_id: UUID = Path(description="Identifier for the client"),
        user_id: UUID = Query(),
    ):
        return await self.client_service.get_client_by_id(organization_id, client_id, user_id)

    @client.patch(
        "/organization/{organization_id}/client/{client_id}",
        tags=["Client"],
        response_model=ClientSchema,
        responses={
            422: {"model": Error, "description": "Unable to process request"},
            404: {"model": Error, "description": "Resource not found"},
            500: {"model": Error, "description": "Server error"},
        },
    )
    async def patch_client_by_id(
        self,
        organization_id: UUID = Path(description="Identifier for the organization"),
        client_id: UUID = Path(description="Identifier for the client"),
        client: ClientUpdateSchema = Body(description="Client request data"),
        user_id: UUID = Query(),
    ):
        return await self.client_service.patch_client_by_id(organization_id, client_id, client)
