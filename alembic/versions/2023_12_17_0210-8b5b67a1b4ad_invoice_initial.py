"""invoice_initial

Revision ID: 8b5b67a1b4ad
Revises: 
Create Date: 2023-12-17 02:10:20.229430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from fastapi_utils.guid_type import GUID

from src.models.invoice import InvoiceStatus, InvoiceType


# revision identifiers, used by Alembic.
revision: str = '8b5b67a1b4ad'
down_revision: Union[str, None] = '8f239109a675'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('invoice', 
                    sa.Column('id', GUID, server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('created', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('modified', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('organization_id', GUID, ForeignKey('organization.id'), nullable=False),
                    sa.Column('type', sa.Enum(InvoiceType), nullable=False),
                    sa.Column('status', sa.Enum(InvoiceStatus), nullable=False),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('invoice')
