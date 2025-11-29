import logging
import uuid

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from account.common.constants import (
    PERMISSIONS,
    ROLES,
    ROLE_PERMISSION_MAPPING,
)
from account.common.enums import OperationTags
from account.models import PermissionModel, PermissionTagsModel, RoleModel
from account.models.association import permission_tags, role_permissions

from utils.database import db_connection, get_db
from utils.schemas import DatabaseSettings, DatabaseURL

logger = logging.getLogger("uvicorn")


def seed_db(url_obj: DatabaseURL, db_settings: DatabaseSettings):
    with get_db(db_connection(url_obj, db_settings)) as db:
        try:
            roles = [
                RoleModel(name=role.name.value, description=role.description)
                for role in ROLES
            ]

            all_permission_tags = [
                PermissionTagsModel(name=tag.value) for tag in OperationTags
            ]

            db.add_all(roles)
            db.add_all(all_permission_tags)
            db.flush()

            for operation_type, permission in PERMISSIONS.items():
                model = PermissionModel(
                    id=uuid.UUID(permission.id),
                    name=permission.name,
                    description=permission.description,
                    type=permission.type,
                    category=permission.category,
                    removable=permission.removable,
                )

                db.add(model)
                db.flush()

                for tag in all_permission_tags:
                    tag_id = None

                    for perm_tag in permission.tags:
                        if tag.name is perm_tag.value:
                            tag_id = tag.id
                            break

                    if tag_id is None:
                        continue

                    stmt = insert(permission_tags).values(
                        permission_id=permission.id, tag_id=tag_id
                    )
                    db.execute(stmt)

                for role in roles:
                    role_permission = ROLE_PERMISSION_MAPPING.get(role.name, None)

                    if role_permission is None:
                        logger.warning(
                            f"Role name '{role.name}' not found in ROLE_PERMISSION_MAPPING. Skipping role"
                        )
                        continue

                    if operation_type not in role_permission:
                        continue

                    stmt = insert(role_permissions).values(
                        role_id=role.id, permission_id=permission.id
                    )
                    db.execute(stmt)

            db.commit()

        except IntegrityError:
            logger.warning(
                "Permissions and roles already inserted. Skipped seeding database"
            )

        except Exception as exc:
            logger.exception(
                "Exception occurred whilst inserting roles and permissions. Rolling back"
            )
            db.rollback()

            raise SystemError("Unable to insert roles and permissions") from exc
