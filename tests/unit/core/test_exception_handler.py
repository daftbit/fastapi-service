import json
from unittest import IsolatedAsyncioTestCase
from urllib.parse import urlencode
import uuid

from fastapi import Request

from src.core.exceptions.exception import DatabaseException, NotFoundException
from src.core.exceptions.exception_handler import (
    database_exception_handler,
    resource_not_found_exception_handler,
)


class TestExceptionHandler(IsolatedAsyncioTestCase):
    async def test_resource_not_found_exception_handler(self):
        organization_id = uuid.uuid4()
        user_id = uuid.uuid4()
        request = Request(
            scope={
                "method": "GET",
                "path": f"https://test-service/v1/organization/{organization_id}",
                "type": "http",
                "query_string": urlencode({"user_id": str(user_id)}).encode("utf-8"),
                "headers": {},
            }
        )

        not_found_exception = NotFoundException(
            "Not found", f"Resource with id {organization_id} not found"
        )

        response = await resource_not_found_exception_handler(
            request, not_found_exception
        )
        self.assertIsNotNone(response)
        response_data = json.loads(response.body.decode("utf-8"))
        self.assertEqual(response_data["error"], "Not found")
        self.assertEqual(
            response_data["message"], f"Resource with id {organization_id} not found"
        )
        self.assertEqual(
            response_data["path"],
            f"https://test-service/v1/organization/{organization_id}?user_id={user_id}",
        )
        self.assertIsNotNone(response_data["timestamp"])
        self.assertEqual(response_data["status"], 404)

    async def test_database_exception_handler(self):
        organization_id = uuid.uuid4()
        user_id = uuid.uuid4()
        request = Request(
            scope={
                "method": "GET",
                "path": f"https://test-service/v1/organization/{organization_id}",
                "type": "http",
                "query_string": urlencode({"user_id": str(user_id)}).encode("utf-8"),
                "headers": {},
            }
        )
        database_exception = DatabaseException(
            "Internal error", "Unable to retrieve organization"
        )
        response = await database_exception_handler(request, database_exception)
        self.assertIsNotNone(response)
        response_data = json.loads(response.body.decode("utf-8"))
        self.assertEqual(response_data["error"], "Internal error")
        self.assertEqual(response_data["message"], "Unable to retrieve organization")
        self.assertEqual(
            response_data["path"],
            f"https://test-service/v1/organization/{organization_id}?user_id={user_id}",
        )
        self.assertIsNotNone(response_data["timestamp"])
        self.assertEqual(response_data["status"], 500)
