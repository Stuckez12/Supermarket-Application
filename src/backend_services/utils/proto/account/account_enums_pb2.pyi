from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class AccountStatusEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNVERIFIED: _ClassVar[AccountStatusEnum]
    INACTIVE: _ClassVar[AccountStatusEnum]
    ACTIVE: _ClassVar[AccountStatusEnum]
    LOCKED: _ClassVar[AccountStatusEnum]
    CLOSED: _ClassVar[AccountStatusEnum]
    TERMINATED: _ClassVar[AccountStatusEnum]

UNVERIFIED: AccountStatusEnum
INACTIVE: AccountStatusEnum
ACTIVE: AccountStatusEnum
LOCKED: AccountStatusEnum
CLOSED: AccountStatusEnum
TERMINATED: AccountStatusEnum
