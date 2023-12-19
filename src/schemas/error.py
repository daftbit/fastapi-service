from pydantic import BaseModel
from pydantic.utils import to_lower_camel


class Error(BaseModel):
    error: str
    message: str
    path: str
    timestamp: str
    status: int

    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True
