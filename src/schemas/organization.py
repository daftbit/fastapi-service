from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from pydantic.utils import to_lower_camel


class OrgnaizationCreateSchema(BaseModel):
    user_id: UUID
    name: str
    email: Optional[str]
    street_address: Optional[str]
    phone_number: Optional[str]

    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class OrganizationSchema(BaseModel):
    id: UUID
    user_id: UUID
    created: datetime
    modified: datetime
    name: str
    street_address: Optional[str]
    phone_number: Optional[str]

    class Config:
        orm_mode = True
        alias_generator = to_lower_camel
        allow_population_by_field_name = True
