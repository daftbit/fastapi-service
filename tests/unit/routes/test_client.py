from datetime import datetime
from unittest import IsolatedAsyncioTestCase, mock
import uuid

from fastapi_pagination import Params, paginate

from httpx import AsyncClient
from src.api import init_api
from src.models.client import Client
from src.repositories.client import ClientRepository
from src.repositories.organization import OrganizationRepository
from src.services.client import ClientService


class TestClient(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.api = init_api()
        self.api.dependency_overrides[OrganizationRepository] = lambda: mock.MagicMock()
        self.api.dependency_overrides[ClientRepository] = lambda: mock.MagicMock()
        self.client = AsyncClient(app=self.api, base_url="https://test-service")

    async def asyncTearDown(self) -> None:
        self.api.dependency_overrides = {}
        await self.client.aclose()

    async def test_create_client_with_missing_name_and_first_name(self):
        organization_id = uuid.uuid4()
        user_id = uuid.uuid4()
        params = [("user_id", str(user_id))]
        request_body = {"firstName": "John"}
        response = await self.client.post(
            f"/v1/organization/{organization_id}/client",
            json=request_body,
            params=params,
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"], "Invalid request")
        self.assertEqual(
            response.json()["message"],
            "name is required when first_name or last_name are absent",
        )
        self.assertEqual(
            response.json()["path"],
            f"https://test-service/v1/organization/{organization_id}/client?user_id={user_id}",
        )
        self.assertIsNotNone(response.json()["timestamp"])
        self.assertEqual(response.json()["status"], 422)

    @mock.patch.object(ClientService, "create_client")
    async def test_create_client(self, mocked_service):
        organization_id = uuid.uuid4()
        user_id = uuid.uuid4()
        params = [("user_id", str(user_id))]
        request_body = {"firstName": "John", "lastName": "Doe"}
        mocked_service.return_value = Client(
            id=uuid.uuid4(),
            organization_id=organization_id,
            created=datetime.now(),
            modified=datetime.now(),
            first_name="John",
            last_name="Doe",
        )
        response = await self.client.post(
            f"/v1/organization/{organization_id}/client",
            json=request_body,
            params=params,
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

    async def test_get_clients_with_missing_user_id(self):
        self.api.dependency_overrides[Params] = lambda: mock.MagicMock()
        organization_id = uuid.uuid4()
        params = []
        response = await self.client.get(
            f"/v1/organization/{organization_id}/client", params=params
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"], "Invalid request")
        self.assertEqual(response.json()["message"], "user_id field required")
        self.assertEqual(
            response.json()["path"],
            f"https://test-service/v1/organization/{organization_id}/client",
        )
        self.assertIsNotNone(response.json()["timestamp"])
        self.assertEqual(response.json()["status"], 422)

    @mock.patch.object(ClientService, "get_clients")
    async def test_get_clients(self, mocked_service):
        self.api.dependency_overrides[Params] = lambda: mock.MagicMock()
        organization_id = uuid.uuid4()
        user_id = uuid.uuid4()
        params = [("user_id", str(user_id))]
        client = Client(
            id=uuid.uuid4(),
            organization_id=organization_id,
            first_name="John",
            last_name="Doe",
        )

        mocked_service.return_value = paginate([client], Params())
        response = await self.client.get(
            f"/v1/organization/{organization_id}/client", params=params
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    async def test_get_client_by_id_with_missing_user_id(self):
        organization_id = uuid.uuid4()
        client_id = uuid.uuid4()
        params = []
        response = await self.client.get(
            f"/v1/organization/{organization_id}/client/{client_id}", params=params
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"], "Invalid request")
        self.assertEqual(response.json()["message"], "user_id field required")
        self.assertEqual(
            response.json()["path"],
            f"https://test-service/v1/organization/{organization_id}/client/{client_id}"
        )
        self.assertIsNotNone(response.json()["timestamp"])
        self.assertEqual(response.json()["status"], 422)

    @mock.patch.object(ClientService, "get_client_by_id")
    async def test_get_client_by_id(self, mocked_service):
        organization_id = uuid.uuid4()
        client_id = uuid.uuid4()
        user_id = uuid.uuid4()
        params = [("user_id", str(user_id))]
        client = Client(
            id=uuid.uuid4(),
            organization_id=organization_id,
            first_name="John",
            last_name="Doe",
        )
        mocked_service.return_value = client
        response = await self.client.get(
            f"/v1/organization/{organization_id}/client/{client_id}", params=params
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
