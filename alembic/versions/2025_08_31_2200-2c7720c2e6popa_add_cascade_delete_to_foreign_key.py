"""Add cascade delete to foreign key

Revision ID: 2c7720c2e6popa
Revises: 2c7720c2e6ce
Create Date: 2025-08-31 22:00:00.000000

"""

from typing import Union, Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2c7720c2e6popa"
down_revision: Union[str, Sequence[str], None] = "2c7720c2e6ce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Удаляем существующий внешний ключ
    op.drop_constraint(
        "fk_blacklisted_tokens_user_id_users", 
        "blacklisted_tokens", 
        type_="foreignkey"
    )
    
    # Создаем новый внешний ключ с каскадным удалением
    op.create_foreign_key(
        "fk_blacklisted_tokens_user_id_users",
        "blacklisted_tokens",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем внешний ключ с каскадным удалением
    op.drop_constraint(
        "fk_blacklisted_tokens_user_id_users", 
        "blacklisted_tokens", 
        type_="foreignkey"
    )
    
    # Восстанавливаем внешний ключ без каскадного удаления
    op.create_foreign_key(
        "fk_blacklisted_tokens_user_id_users",
        "blacklisted_tokens",
        "users",
        ["user_id"],
        ["id"]
    )
