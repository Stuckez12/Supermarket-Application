"""
Initialise database

Revision ID: 0658104e120e
Revises:
Create Date: 2025-12-06 15:56:11.639706
"""

from alembic import op
import sqlalchemy as sa
from typing import Sequence, Union

from utils.database.column_types import EmailType, GenderType, PasswordType


# revision identifiers, used by Alembic.
revision: str = "0658104e120e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "perm_tags",
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "permissions",
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=False),
        sa.Column(
            "type",
            sa.Enum("CREATE", "VIEW", "UPDATE", "DELETE", name="interactiontype"),
            nullable=False,
        ),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("removable", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "roles",
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "accounts",
        sa.Column("email", EmailType(length=96), nullable=False),
        sa.Column("password", PasswordType(), nullable=False),
        sa.Column("password_last_changed_at", sa.DateTime(), nullable=False),
        sa.Column("failed_login_attempts", sa.Integer(), nullable=False),
        sa.Column("account_locked_until", sa.DateTime(), nullable=True),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.Column("master_user", sa.Boolean(), nullable=False),
        sa.Column("first_name", sa.String(length=64), nullable=False),
        sa.Column("last_name", sa.String(length=64), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column(
            "gender",
            GenderType("MALE", "FEMALE", "OTHER", "PREFER_NOT_TO_SAY"),
            nullable=False,
        ),
        sa.Column("email_verified", sa.Boolean(), nullable=False),
        sa.Column(
            "user_status",
            sa.Enum(
                "UNVERIFIED",
                "INACTIVE",
                "ACTIVE",
                "LOCKED",
                "CLOSED",
                "TERMINATED",
                name="accountstatusenum",
            ),
            nullable=False,
        ),
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("password"),
    )
    op.create_table(
        "permission_tags",
        sa.Column("permission_id", sa.UUID(), nullable=False),
        sa.Column("tag_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["permissions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["perm_tags.id"],
        ),
        sa.PrimaryKeyConstraint("permission_id", "tag_id"),
    )
    op.create_table(
        "role_permissions",
        sa.Column("permission_id", sa.UUID(), nullable=False),
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["permissions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.PrimaryKeyConstraint("permission_id", "role_id"),
    )
    op.create_table(
        "account_removed_permissions",
        sa.Column("permission_id", sa.UUID(), nullable=False),
        sa.Column("account_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["accounts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["permissions.id"],
        ),
        sa.PrimaryKeyConstraint("permission_id", "account_id"),
    )


def downgrade() -> None:
    op.drop_table("account_removed_permissions")
    op.drop_table("role_permissions")
    op.drop_table("permission_tags")
    op.drop_table("accounts")
    op.drop_table("roles")
    op.drop_table("permissions")
    op.drop_table("perm_tags")

    op.execute("DROP TYPE IF EXISTS interactiontype;")
    op.execute("DROP TYPE IF EXISTS accountstatusenum;")
    op.execute("DROP TYPE IF EXISTS genderenum;")
