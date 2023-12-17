"""update_modified_time_stamp

Revision ID: be11f0406681
Revises: 8b5b67a1b4ad
Create Date: 2023-12-17 02:26:53.826824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be11f0406681'
down_revision: Union[str, None] = '4857fbd74ba4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE FUNCTION update_modified_time_stamp()"
               "RETURNS TRIGGER AS $$"
               "BEGIN"
               "    NEW.modified = now();"
               "    RETURN NEW;"
               "END;"
               "$$ language 'plpgsql'")


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS update_modified_time_stamp;")
