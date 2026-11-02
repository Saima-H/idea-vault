"""enforce_immutable_audit_logs

Revision ID: ab22782a491f
Revises: 49d6289f770e
Create Date: 2026-11-02 16:38:22.483156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab22782a491f'
down_revision: Union[str, Sequence[str], None] = '49d6289f770e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create a function that prevents any modification or deletion of audit logs
    op.execute("""
        CREATE OR REPLACE FUNCTION prevent_audit_changes()
        RETURNS TRIGGER AS $$
        BEGIN
            RAISE EXCEPTION 'Audit logs are immutable. Modification or deletion is strictly forbidden.';
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Attach the trigger to mark_changes for UPDATE and DELETE
    op.execute("""
        DROP TRIGGER IF EXISTS trigger_prevent_audit_changes ON mark_changes;
        CREATE TRIGGER trigger_prevent_audit_changes
        BEFORE UPDATE OR DELETE ON mark_changes
        FOR EACH ROW
        EXECUTE FUNCTION prevent_audit_changes();
    """)

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trigger_prevent_audit_changes ON mark_changes;")
    op.execute("DROP FUNCTION IF EXISTS prevent_audit_changes();")