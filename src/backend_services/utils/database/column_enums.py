from enum import Enum


class GenderEnum(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    PREFER_NOT_TO_SAY = "Prefer not to say"


class AccountStatusEnum(Enum):
    UNVERIFIED = "Unverified"
    INACTIVE = "Inactive"
    ACTIVE = "Active"
    LOCKED = "Locked"
    CLOSED = "Closed"
    TERMINATED = "Terminated"


class AccountRoleEnum(Enum):
    CUSTOMER = "Customer"
    MODERATOR = "Moderator"
    ADMIN = "Admin"
