import logging

from grpc import ServicerContext
from typing import Self

from account.proto import auth_pb2, auth_pb2_grpc, account_enums_pb2


class AccountAuthService(auth_pb2_grpc.AccountAuthService):
    def AccountRegistration(
        self: Self,
        request: auth_pb2.AccountRegistrationRequest,
        context: ServicerContext,
    ) -> auth_pb2.AccountResponse:
        logging.info("AccountAuthService: AccountRegistration")

        return auth_pb2.AccountResponse(
            id="ID",
            role_id="Role ID",
            first_name="Name",
            last_name="Surname",
            verified=True,
            master_user=True,
            user_status=account_enums_pb2.AccountStatusEnum.ACTIVE,
        )

    def AccountLogin(
        self: Self, request: auth_pb2.AccountLoginRequest, context: ServicerContext
    ) -> auth_pb2.AccountResponse:
        logging.info("AccountAuthService: AccountLogin")

        return auth_pb2.AccountResponse(
            id="ID",
            role_id="Role ID",
            first_name="Name",
            last_name="Surname",
            verified=True,
            master_user=True,
            user_status=account_enums_pb2.AccountStatusEnum.ACTIVE,
        )
