from fastapi import APIRouter
from functools import partial
from google.protobuf.timestamp_pb2 import Timestamp
from uuid import UUID

from gateway.common.dependencies import AccountServiceGRPC
from gateway.schemas import AccountLogin, AccountRegistration, MinimumAccountData

from utils.enums.mappings import ACCOUNT_STATUS_MAPPING, GENDER_ENUM_MAPPING
from utils.mapping import EnumMapping
from utils.proto.account.auth_pb2 import (
    AccountLoginRequest,
    AccountRegistrationRequest,
    AccountResponse,
)
from utils.proto.account.auth_pb2_grpc import AccountAuthServiceStub


api = APIRouter(prefix="/auth", tags=["Account"])


@api.post(
    path="/account/register",
    response_model=MinimumAccountData,
    name="Account Registration",
    description="Gateway to account service to register an account on the application",
)
def post_account_registration(
    request: AccountRegistration, account_service: AccountServiceGRPC
):
    date = Timestamp()
    date.FromDatetime(request.date_of_birth)

    status_mapper = EnumMapping.mapped(ACCOUNT_STATUS_MAPPING)
    gender_mapper = EnumMapping.mapped(GENDER_ENUM_MAPPING)

    data = AccountRegistrationRequest(
        email=request.email,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name,
        date_of_birth=date,
        gender=gender_mapper.get_alternate_enum(request.gender),
    )

    response: AccountResponse = account_service.oto_request(
        request="AccountRegistration",
        stub=partial(AccountAuthServiceStub),
        data=data,
    )

    return MinimumAccountData(
        id=UUID(response.id),
        role_id=UUID(response.role_id),
        first_name=response.first_name,
        last_name=response.last_name,
        verified=response.verified,
        master_user=response.master_user,
        user_status=status_mapper.get_alternate_enum(response.user_status),
    )


@api.post(
    path="/account/login",
    response_model=MinimumAccountData,
    name="Account Login",
    description="Gateway to account service to log in to the application",
)
def post_account_login(request: AccountLogin, account_service: AccountServiceGRPC):
    data = AccountLoginRequest(
        email=request.email,
        password=request.password,
    )

    response: AccountResponse = account_service.oto_request(
        request="AccountLogin",
        stub=partial(AccountAuthServiceStub),
        data=data,
    )

    status_mapper = EnumMapping.mapped(ACCOUNT_STATUS_MAPPING)

    return MinimumAccountData(
        id=UUID(response.id),
        role_id=UUID(response.role_id),
        first_name=response.first_name,
        last_name=response.last_name,
        verified=response.verified,
        master_user=response.master_user,
        user_status=status_mapper.get_alternate_enum(response.user_status),
    )
