from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class GenderEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MALE: _ClassVar[GenderEnum]
    FEMALE: _ClassVar[GenderEnum]
    OTHER: _ClassVar[GenderEnum]
    PREFER_NOT_TO_SAY: _ClassVar[GenderEnum]

MALE: GenderEnum
FEMALE: GenderEnum
OTHER: GenderEnum
PREFER_NOT_TO_SAY: GenderEnum
