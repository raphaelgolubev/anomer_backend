"""Add BlacklistedToken table for token revocation

Revision ID: 52ca6bc4490c
Revises: f523a501cca0
Create Date: 2025-08-14 19:59:38.630433

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "52ca6bc4490c"
down_revision: Union[str, Sequence[str], None] = "f523a501cca0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "blacklisted_tokens",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("jti", sa.String(length=255), nullable=False),
        sa.Column("token_type", sa.String(length=50), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('Europe/Moscow', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('Europe/Moscow', CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_blacklisted_tokens_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_blacklisted_tokens")),
        sa.UniqueConstraint("jti", name=op.f("uq_blacklisted_tokens_jti")),
    )
    op.create_index(
        op.f("ix_blacklisted_tokens_updated_at"),
        "blacklisted_tokens",
        ["updated_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_blacklisted_tokens_updated_at"), table_name="blacklisted_tokens"
    )
    op.drop_table("blacklisted_tokens")
