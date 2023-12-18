"""organization

Revision ID: 4857fbd74ba4
Revises: f32c2b8be7bb
Create Date: 2023-12-17 02:58:39.580820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_utils.guid_type import GUID


# revision identifiers, used by Alembic.
revision: str = '4857fbd74ba4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('organization', 
                    sa.Column('id', GUID, server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('user_id', GUID, nullable=False),
                    sa.Column('created', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('modified', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('name', sa.Text, nullable=False),
                    sa.Column('email', sa.Text),
                    sa.Column('street_address', sa.Text),
                    sa.Column('city', sa.Text),
                    sa.Column('state', sa.Text),
                    sa.Column('zip_code', sa.Text),
                    sa.Column('country', sa.Text),
                    sa.Column('phone_number', sa.Text),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('organization')
