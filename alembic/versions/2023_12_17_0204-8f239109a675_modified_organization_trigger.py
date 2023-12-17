"""modified_organization_trigger

Revision ID: 8f239109a675
Revises: f32c2b8be7bb
Create Date: 2023-12-17 03:08:30.529734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f239109a675'
down_revision: Union[str, None] = 'be11f0406681'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TRIGGER update_organization_modified"
               "    BEFORE UPDATE"
               "    ON"
               "        organization"
               "    FOR EACH ROW "
               "EXECUTE PROCEDURE update_modified_time_stamp();")


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS update_organization_modified ON organization;")