from sqlalchemy import Column, DefaultClause, text, ForeignKey, func, Text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

from src.core.database import Base


class Client(Base):
    __tablename__ = "client"
    id = Column(UUID(as_uuid=True), server_default=DefaultClause(text("gen_random_uuid()")), primary_key=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
    created = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    modified = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    name = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text)
    street_address = Column(Text)
    city = Column(Text)
    state = Column(Text)
    zip_code = Column(Text)
    country = Column(Text)
    phone_number = Column(Text)

    __mapper_args__ = {"eager_defaults": True}
