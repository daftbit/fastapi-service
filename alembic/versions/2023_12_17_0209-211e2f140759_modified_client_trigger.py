"""modified_client_trigger

Revision ID: 211e2f140759
Revises: f32c2b8be7bb
Create Date: 2023-12-17 03:24:12.696189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '211e2f140759'
down_revision: Union[str, None] = 'f32c2b8be7bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TRIGGER update_client_modified"
               "    BEFORE UPDATE"
               "    ON"
               "        client"
               "    FOR EACH ROW "
               "EXECUTE PROCEDURE update_modified_time_stamp();")

def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS update_client_modified ON client;")
