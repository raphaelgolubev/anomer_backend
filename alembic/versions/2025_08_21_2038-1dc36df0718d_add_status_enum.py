"""add status enum

Revision ID: 1dc36df0718d
Revises: a5a562b63894
Create Date: 2025-08-21 20:38:23.628104

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "1dc36df0718d"
down_revision: Union[str, Sequence[str], None] = "a5a562b63894"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    sa.Enum("CREATED", "ACTIVATED", "BANNED", name="userstatus").create(op.get_bind())
    op.add_column(
        "users",
        sa.Column(
            "status",
            postgresql.ENUM(
                "CREATED", "ACTIVATED", "BANNED", name="userstatus", create_type=False
            ),
            server_default="CREATED",
            nullable=False,
        ),
    )
    op.drop_column("users", "is_email_verified")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "is_email_verified",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("users", "status")
    sa.Enum("CREATED", "ACTIVATED", "BANNED", name="userstatus").drop(op.get_bind())
