"""add_audit_log_trigger

Revision ID: 49d6289f770e
Revises: a090cd090bc5
Create Date: 2026-11-02 13:06:13.277343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49d6289f770e'
down_revision: Union[str, Sequence[str], None] = 'a090cd090bc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE OR REPLACE FUNCTION log_mark_change()
        RETURNS TRIGGER AS $$
        BEGIN
            IF OLD.marks_obtained IS DISTINCT FROM NEW.marks_obtained THEN
                INSERT INTO mark_changes (
                    question_mark_id, 
                    old_marks, 
                    new_marks, 
                    changed_by
                ) VALUES (
                    OLD.id, 
                    OLD.marks_obtained, 
                    NEW.marks_obtained, 
                    COALESCE(current_setting('app.current_user', true), 'System_Teacher')
                );
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        DROP TRIGGER IF EXISTS trigger_log_mark_change ON question_marks;
        CREATE TRIGGER trigger_log_mark_change
        AFTER UPDATE ON question_marks
        FOR EACH ROW
        EXECUTE FUNCTION log_mark_change();
    """)

    op.execute("""
        REVOKE UPDATE, DELETE ON mark_changes FROM PUBLIC;
        REVOKE UPDATE, DELETE ON mark_changes FROM postgres;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trigger_log_mark_change ON question_marks;")
    op.execute("DROP FUNCTION IF EXISTS log_mark_change();")
    op.execute("GRANT UPDATE, DELETE ON mark_changes TO PUBLIC;")
    op.execute("GRANT UPDATE, DELETE ON mark_changes TO postgres;")