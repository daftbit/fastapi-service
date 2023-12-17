"""client_initial

Revision ID: f32c2b8be7bb
Revises: b6fbe4de4edd
Create Date: 2023-12-17 02:46:46.758110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from fastapi_utils.guid_type import GUID


# revision identifiers, used by Alembic.
revision: str = 'f32c2b8be7bb'
down_revision: Union[str, None] = 'b6fbe4de4edd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('client',
                    sa.Column('id', GUID, server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('invoice_id', GUID, ForeignKey('invoice.id'), nullable=False),
                    sa.Column('created', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('modified', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('organization_name', sa.Text),
                    sa.Column('first_name', sa.Text),
                    sa.Column('last_name', sa.Text),
                    sa.Column('email', sa.Text),
                    sa.Column('street_address', sa.Text),
                    sa.Column('phone_numeber', sa.Text),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('client')
