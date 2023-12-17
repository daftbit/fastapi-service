"""modified_invoice_trigger

Revision ID: b6fbe4de4edd
Revises: be11f0406681
Create Date: 2023-12-17 02:32:05.305960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6fbe4de4edd'
down_revision: Union[str, None] = '8b5b67a1b4ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TRIGGER update_invoice_modified"
               "    BEFORE UPDATE"
               "    ON"
               "        invoice"
               "    FOR EACH ROW "
               "EXECUTE PROCEDURE update_modified_time_stamp();")


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS update_invoice_modified ON invoice;")
