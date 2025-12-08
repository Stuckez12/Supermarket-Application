"""
Adding initial constraints

Revision ID: 283232f704e1
Revises: 0658104e120e
Create Date: 2025-12-08 21:33:47.130197
"""

from alembic import op
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "283232f704e1"
down_revision: Union[str, Sequence[str], None] = "0658104e120e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("account_id_unique_constraint", "accounts", ["id"])
    op.create_unique_constraint("perm_tags_id_unique_constraint", "perm_tags", ["id"])
    op.create_unique_constraint(
        "permissions_id_unique_constraint", "permissions", ["id"]
    )
    op.create_unique_constraint("roles_id_unique_constraint", "roles", ["id"])


def downgrade() -> None:
    op.drop_constraint("roles_id_unique_constraint", "roles", type_="unique")
    op.drop_constraint(
        "permissions_id_unique_constraint", "permissions", type_="unique"
    )
    op.drop_constraint("perm_tags_id_unique_constraint", "perm_tags", type_="unique")
    op.drop_constraint("account_id_unique_constraint", "accounts", type_="unique")
