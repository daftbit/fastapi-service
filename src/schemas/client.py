from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel, root_validator

from pydantic.utils import to_lower_camel


class ClientCreateSchema(BaseModel):
    name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    street_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    country: Optional[str]
    phone_number: Optional[str]

    @root_validator(pre=True)
    def validate_client_schema(cls, values):
        name, first_name, last_name = (
            values.get("name", None),
            values.get("firstName", None),
            values.get("lastName", None),
        )
        print("Name", name)
        print("First name", first_name)
        print("Last Name", last_name)
        if name is None and first_name is None or last_name is None:
            raise ValueError("name is required when first_name or last_name are absent")
        return values

    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class ClientUpdateSchema(BaseModel):
    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class ClientSchema(BaseModel):
    id: UUID
    organization_id: UUID
    name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    street_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    country: Optional[str]
    phone_number: Optional[str]

    class Config:
        orm_mode = True
        alias_generator = to_lower_camel
        allow_population_by_field_name = True
