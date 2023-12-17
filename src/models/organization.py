from sqlalchemy import Column, DefaultClause, text, func, Text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

from src.core.database import Base


class Organization(Base):
    __tablename__ = "organization"

    id = Column(UUID(as_uuid=True), server_default=DefaultClause(text("gen_random_uuid()")), primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    modified = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    name = Column(Text, nullable=False)
    email = Column(Text)
    street_address = Column(Text)
    phone_number = Column(Text)
