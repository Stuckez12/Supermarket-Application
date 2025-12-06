from google.protobuf import timestamp_pb2 as _timestamp_pb2
from account.proto import account_enums_pb2 as _account_enums_pb2
from account.proto import common_enums_pb2 as _common_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class AccountResponse(_message.Message):
    __slots__ = (
        "id",
        "role_id",
        "first_name",
        "last_name",
        "verified",
        "master_user",
        "user_status",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    MASTER_USER_FIELD_NUMBER: _ClassVar[int]
    USER_STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    role_id: str
    first_name: str
    last_name: str
    verified: bool
    master_user: bool
    user_status: _account_enums_pb2.AccountStatusEnum
    def __init__(
        self,
        id: _Optional[str] = ...,
        role_id: _Optional[str] = ...,
        first_name: _Optional[str] = ...,
        last_name: _Optional[str] = ...,
        verified: bool = ...,
        master_user: bool = ...,
        user_status: _Optional[_Union[_account_enums_pb2.AccountStatusEnum, str]] = ...,
    ) -> None: ...

class AccountRegistrationRequest(_message.Message):
    __slots__ = (
        "email",
        "password",
        "first_name",
        "last_name",
        "date_of_birth",
        "gender",
    )
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    DATE_OF_BIRTH_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: _timestamp_pb2.Timestamp
    gender: _common_enums_pb2.GenderEnum
    def __init__(
        self,
        email: _Optional[str] = ...,
        password: _Optional[str] = ...,
        first_name: _Optional[str] = ...,
        last_name: _Optional[str] = ...,
        date_of_birth: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        gender: _Optional[_Union[_common_enums_pb2.GenderEnum, str]] = ...,
    ) -> None: ...

class AccountLoginRequest(_message.Message):
    __slots__ = ("email", "password")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    def __init__(
        self, email: _Optional[str] = ..., password: _Optional[str] = ...
    ) -> None: ...
