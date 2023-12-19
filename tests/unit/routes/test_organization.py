from datetime import datetime
from unittest import IsolatedAsyncioTestCase, mock
import uuid
from fastapi_pagination import Params, paginate

from httpx import AsyncClient

from src.api import init_api
from src.models.organization import Organization
from src.repositories.organization import OrganizationRepository
from src.schemas.organization import OrganizationUpdateSchema
from src.services.organization import OrganizationService


class TestOrganization(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.api = init_api()
        self.api.dependency_overrides[OrganizationRepository] = lambda: mock.MagicMock()
        self.client = AsyncClient(app=self.api, base_url="https://test-service")

    async def asyncTearDown(self) -> None:
        self.api.dependency_overrides = {}
        await self.client.aclose()

    async def test_create_organization_with_missing_name(self):
        request_body = {
            "userId": str(uuid.uuid4()),
            "email": "wonderful.widgets@wonderful-widgets.com",
            "streetAddress": "123 Main St.",
            "city": "AnyTown",
            "state": "AnyState",
            "zipCode": "54321",
            "country": "US",
            "phoneNumber": "(555)-555-5555",
        }
        response = await self.client.post("/v1/organization", json=request_body)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"], "Invalid request")
        self.assertEqual(response.json()["message"], "name field required")
        self.assertEqual(
            response.json()["path"], "https://test-service/v1/organization"
        )
        self.assertIsNotNone(response.json()["timestamp"])
        self.assertEqual(response.json()["status"], 422)

    @mock.patch.object(OrganizationService, "create_organization")
    async def test_create_organization(self, mocked_service):
        request_body = {
            "userId": str(uuid.uuid4()),
            "name": "Wonderful Widgets",
            "email": "wonderful.widgets@wonderful-widgets.com",
            "streetAddress": "123 Main St.",
            "city": "AnyTown",
            "state": "AnyState",
            "zipCode": "54321",
            "country": "US",
            "phoneNumber": "(555)-555-5555",
        }
        mocked_service.return_value = Organization(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            created=datetime.now(),
            modified=datetime.now(),
            name="Wonderful Widgets",
            email="wonderful.widgets@wonderful-widgets.com",
            street_address="123 Main St.",
            city="AnyTown",
            state="AnyState",
            zip_code="54321",
            country="US",
            phone_number="(555)-555-5555",
        )

        response = await self.client.post("/v1/organization", json=request_body)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

    async def test_get_organizations_with_missing_user_id(self):
        self.api.dependency_overrides[Params] = lambda: mock.MagicMock()
        params = []
        response = await self.client.get("/v1/organization", params=params)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"], "Invalid request")
        self.assertEqual(response.json()["message"], "user_id field required")
        self.assertEqual(
            response.json()["path"], "https://test-service/v1/organization"
        )
        self.assertIsNotNone(response.json()["timestamp"])
        self.assertEqual(response.json()["status"], 422)

    @mock.patch.object(OrganizationService, "get_organizations")
    async def test_get_organizations(self, mocked_service):
        self.api.dependency_overrides[Params] = lambda: mock.MagicMock()
        params = [("user_id", str(uuid.uuid4()))]

        organization = Organization(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            created=datetime.now(),
            modified=datetime.now(),
            name="Wonderful Widgets",
            email="wonderful.widgets@wonderful-widgets.com",
            street_address="123 Main St.",
            city="AnyTown",
            state="AnyState",
            zip_code="54321",
            country="US",
            phone_number="(555)-555-5555",
        )

        mocked_service.return_value = paginate([organization], Params())

        response = await self.client.get("/v1/organization", params=params)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    async def test_get_organization_by_id_with_invalid_organization_id(self):
        user_id = str(uuid.uuid4())
        params = [("user_id", user_id)]

        response = await self.client.get("/v1/organization/1", params=params)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"], "Invalid request")
        self.assertEqual(
            response.json()["message"], "organization_id value is not a valid uuid"
        )
        self.assertEqual(
            response.json()["path"],
            f"https://test-service/v1/organization/1?user_id={user_id}",
        )
        self.assertIsNotNone(response.json()["timestamp"])
        self.assertEqual(response.json()["status"], 422)

    @mock.patch.object(OrganizationService, "get_organization_by_id")
    async def test_get_organization_by_id(self, mocked_service):
        organization_id = uuid.uuid4()
        params = [("user_id", str(uuid.uuid4()))]

        organization = Organization(
            id=organization_id,
            user_id=uuid.uuid4(),
            created=datetime.now(),
            modified=datetime.now(),
            name="Wonderful Widgets",
            email="wonderful.widgets@wonderful-widgets.com",
            street_address="123 Main St.",
            city="AnyTown",
            state="AnyState",
            zip_code="54321",
            country="US",
            phone_number="(555)-555-5555",
        )
        mocked_service.return_value = organization

        response = await self.client.get(
            f"/v1/organization/{organization_id}", params=params
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(OrganizationService, "patch_organization_by_id")
    async def test_patch_organization_by_id(self, mocked_service):
        organization_id = uuid.uuid4()
        user_id = uuid.uuid4()
        params = [("user_id", str(user_id))]

        request_body = OrganizationUpdateSchema(
            city="SomeTown", state="SomeState", zip_code="12345"
        )

        mocked_service.return_value = Organization(
            id=organization_id,
            user_id=uuid.uuid4(),
            created=datetime.now(),
            modified=datetime.now(),
            name="Wonderful Widgets",
            email="wonderful.widgets@wonderful-widgets.com",
            street_address="123 Main St.",
            city="SomeTown",
            state="SomeState",
            zip_code="12345",
            country="US",
            phone_number="(555)-555-5555",
        )
        response = await self.client.patch(
            f"/v1/organization/{organization_id}",
            params=params,
            json=request_body.dict(),
        )

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
