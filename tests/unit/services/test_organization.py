from datetime import datetime
from unittest import IsolatedAsyncioTestCase, mock
import uuid

from fastapi_pagination import paginate, Params
from src.models.organization import Organization

from src.repositories.organization import OrganizationRepository
from src.schemas.organization import OrganizationCreateSchema, OrganizationUpdateSchema
from src.services.organization import OrganizationService


class TestOrganizationService(IsolatedAsyncioTestCase):
    @mock.patch.object(OrganizationRepository, "create_organization")
    async def test_create_organization(self, mocked_repository):
        user_id = uuid.uuid4()
        organization = OrganizationCreateSchema(
            user_id=user_id,
            name="Wonderful Widgets",
            email="wonderful.widgets@wonderful-widgets.com",
            street_address="123 Main St.",
            city="AnyTown",
            state="AnyState",
            zip_code="54321",
            country="US",
            phone_number="(555) 555-5555",
        )
        service = OrganizationService(mocked_repository)

        result = await service.create_organization(organization)
        self.assertIsNotNone(result)

    @mock.patch.object(OrganizationRepository, "get_organizations")
    async def test_get_organizations(self, mocked_repository):
        user_id = uuid.uuid4()
        organization_id = uuid.uuid4()
        organization = Organization(
            id=organization_id,
            user_id=user_id,
            created=datetime.now(),
            modified=datetime.now(),
            name="Wonderful Widgets",
            email="wonderful.widgets@wonderful-widgets.com",
            street_address="123 Main St.",
            city="AnyTown",
            state="AnyState",
            zip_code="54321",
            country="US",
            phone_number="(555) 555-5555",
        )
        mocked_repository.return_value = paginate([organization], Params())

        service = OrganizationService(mocked_repository)
        result = await service.get_organizations(Params(), user_id)
        self.assertIsNotNone(result)

    @mock.patch.object(OrganizationRepository, "get_organization_by_id")
    async def test_get_organization_by_id(self, mocked_repository):
        user_id = uuid.uuid4()
        organization_id = uuid.uuid4()
        mocked_repository.return_value = Organization(
            id=organization_id,
            user_id=user_id,
            created=datetime.now(),
            modified=datetime.now(),
            name="Wonderful Widgets",
            email="wonderful.widgets@wonderful-widgets.com",
            street_address="123 Main St.",
            city="AnyTown",
            state="AnyState",
            zip_code="54321",
            country="US",
            phone_number="(555) 555-5555",
        )
        service = OrganizationService(mocked_repository)
        result = await service.get_organization_by_id(organization_id, user_id)
        self.assertIsNotNone(result)

    @mock.patch.object(OrganizationRepository, "patch_organization_by_id")
    async def test_patch_organization_by_id(self, mocked_repository):
        user_id = uuid.uuid4()
        organization_id = uuid.uuid4()
        organization_update_schema = OrganizationUpdateSchema(
            city="SomeTown", state="SomeState", zip_code="12345"
        )
        mocked_repository.return_value = Organization(
            id=organization_id,
            user_id=user_id,
            created=datetime.now(),
            modified=datetime.now(),
            name="Wonderful Widgets",
            email="wonderful.widgets@wonderful-widgets.com",
            street_address="123 Main St.",
            city="SomeTown",
            state="SomeState",
            zip_code="12345",
            country="US",
            phone_number="(555) 555-5555",
        )
        service = OrganizationService(mocked_repository)
        result = await service.patch_organization_by_id(
            organization_id, organization_update_schema, user_id
        )
        self.assertIsNotNone(result)
