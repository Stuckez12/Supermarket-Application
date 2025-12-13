from account.common.enums import InteractionType, OperationTags, OperationType
from account.schemas import PermissionCreateSchema, RoleMappingSchema

from utils.enums.enums import AccountRoleEnum


ACCOUNT_SERVICE_VERSION = "0.0.1"


PERMISSIONS = {
    OperationType.ADMIN_CREATE_ACCOUNT: PermissionCreateSchema(
        id=OperationType.ADMIN_CREATE_ACCOUNT.value,
        name=OperationType.ADMIN_CREATE_ACCOUNT.name,
        description="Allows Admins to create accounts on behalf of other users",
        type=InteractionType.CREATE,
        category="Account Management",
        tags=[
            OperationTags.ADMIN,
            OperationTags.ACCOUNT,
            OperationTags.MANAGEMENT,
            OperationTags.CREATE,
        ],
        removable=True,
    ),
    OperationType.ADMIN_UPDATE_ACCOUNT: PermissionCreateSchema(
        id=OperationType.ADMIN_UPDATE_ACCOUNT.value,
        name=OperationType.ADMIN_UPDATE_ACCOUNT.name,
        description="Allows Admins to update account details on behalf of other users",
        type=InteractionType.UPDATE,
        category="Account Management",
        tags=[
            OperationTags.ADMIN,
            OperationTags.ACCOUNT,
            OperationTags.MANAGEMENT,
            OperationTags.UPDATE,
        ],
        removable=True,
    ),
    OperationType.ADMIN_UPDATE_ACCOUNT_SETTINGS: PermissionCreateSchema(
        id=OperationType.ADMIN_UPDATE_ACCOUNT_SETTINGS.value,
        name=OperationType.ADMIN_UPDATE_ACCOUNT_SETTINGS.name,
        description="Allows Admins to update account settings on behalf of other users",
        type=InteractionType.UPDATE,
        category="Account Management",
        tags=[
            OperationTags.ADMIN,
            OperationTags.ACCOUNT,
            OperationTags.MANAGEMENT,
            OperationTags.UPDATE,
        ],
        removable=True,
    ),
    OperationType.ADMIN_VIEW_ACCOUNT: PermissionCreateSchema(
        id=OperationType.ADMIN_VIEW_ACCOUNT.value,
        name=OperationType.ADMIN_VIEW_ACCOUNT.name,
        description="Allows Admins to view account details of other users",
        type=InteractionType.VIEW,
        category="Account Management",
        tags=[
            OperationTags.ADMIN,
            OperationTags.ACCOUNT,
            OperationTags.MANAGEMENT,
            OperationTags.VIEW,
        ],
        removable=True,
    ),
    OperationType.ADMIN_VIEW_ACCOUNT_SETTINGS: PermissionCreateSchema(
        id=OperationType.ADMIN_VIEW_ACCOUNT_SETTINGS.value,
        name=OperationType.ADMIN_VIEW_ACCOUNT_SETTINGS.name,
        description="Allows Admins to view account settings of other users",
        type=InteractionType.VIEW,
        category="Account Management",
        tags=[
            OperationTags.ADMIN,
            OperationTags.ACCOUNT,
            OperationTags.MANAGEMENT,
            OperationTags.VIEW,
        ],
        removable=True,
    ),
    OperationType.ADMIN_VERIFY_ACCOUNT: PermissionCreateSchema(
        id=OperationType.ADMIN_VERIFY_ACCOUNT.value,
        name=OperationType.ADMIN_VERIFY_ACCOUNT.name,
        description="Allows Admins to verify accounts on behalf of other users",
        type=InteractionType.UPDATE,
        category="Account Management",
        tags=[
            OperationTags.ADMIN,
            OperationTags.ACCOUNT,
            OperationTags.MANAGEMENT,
            OperationTags.UPDATE,
        ],
        removable=True,
    ),
    OperationType.ADMIN_MODIFY_ACCOUNT_STATUS: PermissionCreateSchema(
        id=OperationType.ADMIN_MODIFY_ACCOUNT_STATUS.value,
        name=OperationType.ADMIN_MODIFY_ACCOUNT_STATUS.name,
        description="Allows Admins to change an accounts' status",
        type=InteractionType.UPDATE,
        category="Account Management",
        tags=[
            OperationTags.ADMIN,
            OperationTags.ACCOUNT,
            OperationTags.MANAGEMENT,
            OperationTags.UPDATE,
        ],
        removable=True,
    ),
    OperationType.ADMIN_LOCK_ACCOUNT_ROLE: PermissionCreateSchema(
        id=OperationType.ADMIN_LOCK_ACCOUNT_ROLE.value,
        name=OperationType.ADMIN_LOCK_ACCOUNT_ROLE.name,
        description="Allows Admins to lock accounts",
        type=InteractionType.UPDATE,
        category="Account Management",
        tags=[
            OperationTags.ADMIN,
            OperationTags.ACCOUNT,
            OperationTags.MANAGEMENT,
            OperationTags.UPDATE,
        ],
        removable=True,
    ),
    OperationType.ADMIN_UNLOCK_ACCOUNT_ROLE: PermissionCreateSchema(
        id=OperationType.ADMIN_UNLOCK_ACCOUNT_ROLE.value,
        name=OperationType.ADMIN_UNLOCK_ACCOUNT_ROLE.name,
        description="Allows Admins to unlock accounts",
        type=InteractionType.UPDATE,
        category="Account Management",
        tags=[
            OperationTags.ADMIN,
            OperationTags.ACCOUNT,
            OperationTags.MANAGEMENT,
            OperationTags.UPDATE,
        ],
        removable=True,
    ),
    OperationType.VIEW_ACCOUNT: PermissionCreateSchema(
        id=OperationType.VIEW_ACCOUNT.value,
        name=OperationType.VIEW_ACCOUNT.name,
        description="Allows users to view their account details",
        type=InteractionType.VIEW,
        category="Account",
        tags=[
            OperationTags.ACCOUNT,
            OperationTags.VIEW,
        ],
    ),
    OperationType.UPDATE_ACCOUNT: PermissionCreateSchema(
        id=OperationType.UPDATE_ACCOUNT.value,
        name=OperationType.UPDATE_ACCOUNT.name,
        description="Allows users to update their account",
        type=InteractionType.UPDATE,
        category="Account",
        tags=[
            OperationTags.ACCOUNT,
            OperationTags.MANAGEMENT,
            OperationTags.UPDATE,
        ],
    ),
    OperationType.DELETE_ACCOUNT: PermissionCreateSchema(
        id=OperationType.DELETE_ACCOUNT.value,
        name=OperationType.DELETE_ACCOUNT.name,
        description="Allows users to 'delete' their account",
        type=InteractionType.DELETE,
        category="Account",
        tags=[
            OperationTags.ACCOUNT,
            OperationTags.MANAGEMENT,
            OperationTags.DELETE,
        ],
    ),
}


CUSTOMER_ROLE_PERMISSIONS = [
    OperationType.VIEW_ACCOUNT,
    OperationType.UPDATE_ACCOUNT,
    OperationType.DELETE_ACCOUNT,
]


MODERATOR_ROLE_PERMISSIONS = CUSTOMER_ROLE_PERMISSIONS + [
    OperationType.ADMIN_VIEW_ACCOUNT,
    OperationType.ADMIN_MODIFY_ACCOUNT_STATUS,
]


ADMIN_ROLE_PERMISSIONS = [p for p in OperationType]


ROLE_PERMISSION_MAPPING = {
    AccountRoleEnum.ADMIN.value: ADMIN_ROLE_PERMISSIONS,
    AccountRoleEnum.MODERATOR.value: MODERATOR_ROLE_PERMISSIONS,
    AccountRoleEnum.CUSTOMER.value: CUSTOMER_ROLE_PERMISSIONS,
}


ROLES = [
    RoleMappingSchema(
        name=AccountRoleEnum.ADMIN,
        description="Admin users monitor and upkeep the sites' health and operations with full access to the application functionality",
    ),
    RoleMappingSchema(
        name=AccountRoleEnum.MODERATOR,
        description="Moderator users enforce the sites' rules and regulations on all customer users",
    ),
    RoleMappingSchema(
        name=AccountRoleEnum.CUSTOMER,
        description="Customer users interact with the site to browse, shop, and manage their personal account",
    ),
]
