from uuid import UUID
from fastapi import Depends
from fastapi_pagination import Params, paginate
from fastapi_pagination.bases import AbstractPage
from sqlalchemy import select
from sqlalchemy.exc import StatementError
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import Database


from src.models.organization import Organization
from src.schemas.organization import OrgnaizationCreateSchema


class OrganizationRepository:
    def __init__(self, session: AsyncSession = Depends(Database.session)):
        self.session = session

    async def create_organization(self, organization: OrgnaizationCreateSchema) -> Organization:
        new_organization = Organization(**organization.dict())
        try:
            async with self.session as session:
                async with session.begin():
                    session.add(new_organization)
                await session.refresh(new_organization)
            return new_organization
        except StatementError as exc:
            # TODO: log error and raise exception to be caught by exception handler
            pass

    async def get_organizations(self, page_params: Params, user_id: UUID) -> AbstractPage[Organization]:
        try:
            async with self.session as session:
                query = select(Organization).where(Organization.user_id == user_id).order_by(Organization.modified.desc())
                q = await session.execute(query)
            return paginate(q.scalars().unique().all(), page_params)
        except StatementError as exc:
            # TODO: log error and raise exception to be caught by exception handler
            pass
