import logging

from enum import Enum


logger = logging.getLogger("uvicorn")


class InteractionType(Enum):
    CREATE = "Create"
    VIEW = "View"
    UPDATE = "Update"
    DELETE = "Delete"


class OperationTags(Enum):
    CREATE = "Create"
    VIEW = "View"
    UPDATE = "Update"
    DELETE = "Delete"
    ADMIN = "Admin"
    ACCOUNT = "Account"
    MANAGEMENT = "Management"


class OperationType(Enum):
    # Personal account interaction
    VIEW_ACCOUNT = "bf9ee575-95ea-4fea-b084-bd078757cb6b"
    UPDATE_ACCOUNT = "845291fc-a869-496b-b276-67e7dece5c97"
    DELETE_ACCOUNT = "baef119e-1990-4399-a7b3-ed711d14362d"

    # Admin account interaction
    ADMIN_CREATE_ACCOUNT = "f2090883-3afc-48f9-bc06-09c33dca3282"
    ADMIN_UPDATE_ACCOUNT = "00d88f5d-bddd-47cb-ab16-5e9bf5a27a49"
    ADMIN_UPDATE_ACCOUNT_SETTINGS = "e923e5c6-01da-40ca-a999-2eaf4f108549"
    ADMIN_VIEW_ACCOUNT = "a1cf6de2-fb29-4323-8790-e4ba55e273d2"
    ADMIN_VIEW_ACCOUNT_SETTINGS = "16058c1a-ca48-4ed1-ba88-d9d01c1c9078"
    ADMIN_VERIFY_ACCOUNT = "f741052f-e745-4347-ab1c-616dabdee805"
    ADMIN_MODIFY_ACCOUNT_STATUS = "404efa3b-99df-403d-b22c-f0fcfafc476e"
    ADMIN_MODIFY_ACCOUNT_ROLE = "6ed89696-4463-4770-9d3c-ac9d0acaef78"
    ADMIN_LOCK_ACCOUNT_ROLE = "962741be-789c-4db5-855d-9df8416b4497"
    ADMIN_UNLOCK_ACCOUNT_ROLE = "bb89f8b3-c6e1-485e-956c-7e9c86c5f906"
