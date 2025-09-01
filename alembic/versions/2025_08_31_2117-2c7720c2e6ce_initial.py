"""initial

Revision ID: 2c7720c2e6ce
Revises:
Create Date: 2025-08-31 21:17:01.735969

"""

from typing import Union, Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "2c7720c2e6ce"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("role", sa.String(), server_default="USER", nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "CREATED", "WAIT_ACTIVATION", "ACTIVATED", "BANNED", name="userstatus"
            ),
            server_default="CREATED",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.BigInteger(),
            server_default=sa.text("EXTRACT(EPOCH FROM NOW())::INTEGER"),
            nullable=False,
            comment="Unix timestamp создания записи (секунды от epoch)",
        ),
        sa.Column(
            "updated_at",
            sa.BigInteger(),
            server_default=sa.text("EXTRACT(EPOCH FROM NOW())::INTEGER"),
            nullable=True,
            comment="Unix timestamp последнего обновления записи (секунды от epoch)",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )
    op.create_index(op.f("ix_users_updated_at"), "users", ["updated_at"], unique=False)
    op.create_table(
        "blacklisted_tokens",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("jti", sa.String(length=255), nullable=False),
        sa.Column("token_type", sa.String(length=50), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("expires_at", sa.BigInteger(), nullable=False),
        sa.Column(
            "created_at",
            sa.BigInteger(),
            server_default=sa.text("EXTRACT(EPOCH FROM NOW())::INTEGER"),
            nullable=False,
            comment="Unix timestamp создания записи (секунды от epoch)",
        ),
        sa.Column(
            "updated_at",
            sa.BigInteger(),
            server_default=sa.text("EXTRACT(EPOCH FROM NOW())::INTEGER"),
            nullable=True,
            comment="Unix timestamp последнего обновления записи (секунды от epoch)",
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
    op.drop_index(op.f("ix_users_updated_at"), table_name="users")
    op.drop_table("users")
