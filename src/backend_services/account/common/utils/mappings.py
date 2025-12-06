from account.proto.account_enums_pb2 import AccountStatusEnum as GRPCAccountStatusEnum
from account.proto.common_enums_pb2 import GenderEnum as GRPCGenderEnum

from utils.enums import (
    AccountStatusEnum as PythonAccountStatusEnum,
    GenderEnum as PythonGenderEnum,
)


GENDER_ENUM_MAPPING: dict[GRPCGenderEnum, PythonGenderEnum] = {
    GRPCGenderEnum.MALE: PythonGenderEnum.MALE,
    GRPCGenderEnum.FEMALE: PythonGenderEnum.FEMALE,
    GRPCGenderEnum.OTHER: PythonGenderEnum.OTHER,
    GRPCGenderEnum.PREFER_NOT_TO_SAY: PythonGenderEnum.PREFER_NOT_TO_SAY,
}

ACCOUNT_STATUS_MAPPING: dict[GRPCGenderEnum, PythonGenderEnum] = {
    PythonAccountStatusEnum.ACTIVE: GRPCAccountStatusEnum.ACTIVE,
    PythonAccountStatusEnum.INACTIVE: GRPCAccountStatusEnum.INACTIVE,
    PythonAccountStatusEnum.UNVERIFIED: GRPCAccountStatusEnum.UNVERIFIED,
    PythonAccountStatusEnum.CLOSED: GRPCAccountStatusEnum.CLOSED,
    PythonAccountStatusEnum.LOCKED: GRPCAccountStatusEnum.LOCKED,
    PythonAccountStatusEnum.TERMINATED: GRPCAccountStatusEnum.TERMINATED,
}
