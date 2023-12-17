import enum

from sqlalchemy import Column, DefaultClause, text, func, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

from src.core.database import Base


class InvoiceType(enum.Enum):
    ESTIMATE = "estimate"
    SALE = "sale"


class InvoiceStatus(enum.Enum):
    INITIAL = "initial"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BILLED = "billed"
    PAID = "paid"


class Invoice(Base):
    __tablename__ = "invoice"
    id = Column(UUID(as_uuid=True), server_default=DefaultClause(text("gen_random_uuid()")), primary_key=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
    created = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    modified = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    type = Column(enum.Enum(InvoiceType), nullable=False)
    status = Column(enum.Enum(InvoiceStatus), nullable=False)
