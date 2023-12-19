from uuid import UUID
from fastapi import Depends
from fastapi_pagination import Params, paginate
from fastapi_pagination.bases import AbstractPage
from sqlalchemy import select, and_
from sqlalchemy.exc import StatementError
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import Database
from src.core.exceptions.exception import DatabaseException, NotFoundException


from src.models.organization import Organization
from src.schemas.organization import OrganizationCreateSchema, OrganizationUpdateSchema


class OrganizationRepository:
    def __init__(self, session: AsyncSession = Depends(Database.session)):
        self.session = session

    async def create_organization(self, organization: OrganizationCreateSchema) -> Organization:
        new_organization = Organization(**organization.dict())
        try:
            async with self.session as session:
                async with session.begin():
                    session.add(new_organization)
                await session.refresh(new_organization)
            return new_organization
        except StatementError as exc:
            # TODO: log error
            raise DatabaseException("Internal error", "Unable to create organization") from exc

    async def get_organizations(self, page_params: Params, user_id: UUID) -> AbstractPage[Organization]:
        try:
            async with self.session as session:
                async with session.begin():
                    query = (
                        select(Organization)
                        .where(Organization.user_id == user_id)
                        .order_by(Organization.modified.desc())
                    )
                    q = await session.execute(query)
            return paginate(q.scalars().unique().all(), page_params)
        except StatementError as exc:
            # TODO: log error
            raise DatabaseException("Internal error", "Unable to retreieve organizations") from exc

    async def get_organization_by_id(self, organization_id: UUID, user_id: UUID) -> Organization:
        try:
            async with self.session as session:
                async with session.begin():
                    query = select(Organization).filter(
                        and_(Organization.id == organization_id, Organization.user_id == user_id)
                    )
                    q = await session.execute(query)
            existing_organization = q.scalars().first()
            if existing_organization is None:
                # TODO log error
                raise NotFoundException("Not found", f"Resource with id {str(organization_id)} not found")
            return existing_organization
        except StatementError as exc:
            # TODO log error
            raise DatabaseException("Internal error", "Unable to retrieve organization") from exc

    async def patch_organization_by_id(
        self, organization_id: UUID, organization: OrganizationUpdateSchema, user_id: UUID
    ) -> Organization:
        try:
            async with self.session as session:
                async with session.begin():
                    query = select(Organization).filter(
                        and_(Organization.id == organization_id, Organization.user_id == user_id)
                    )
                    q = await session.execute(query)
                    existing_organization = q.scalars().first()
                    if existing_organization is None:
                        raise NotFoundException("Not found", f"Resource with id {str(organization_id)} not found")

                    for column, value in organization.dict(exclude_unset=True).items():
                        setattr(existing_organization, column, value)
                await self.session.refresh(existing_organization)
            return existing_organization
        except StatementError as exc:
            raise DatabaseException("Internal error", "Unable to update organization") from exc
