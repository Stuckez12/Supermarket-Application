import logging

from datetime import datetime, timedelta
from grpc import ServicerContext, StatusCode
from sqlalchemy.exc import NoResultFound
from typing import Self

from account.proto import auth_pb2, auth_pb2_grpc
from account.common.utils import get_db_gen, ACCOUNT_STATUS_MAPPING, GENDER_ENUM_MAPPING
from account.models import AccountModel, RoleModel

from utils.constants import (
    EMAIL_CONFIG,
    FIRST_NAME_CONFIG,
    LAST_NAME_CONFIG,
    PASSWORD_CONFIG,
)
from utils.data_verification import DataVerification
from utils.enums import AccountRoleEnum, AccountStatusEnum
from utils.mapping import PythonGRPCMapping
from utils.schemas.data_verification import DateTimeConfig


class AccountAuthService(auth_pb2_grpc.AccountAuthService):
    def AccountRegistration(
        self: Self,
        request: auth_pb2.AccountRegistrationRequest,
        context: ServicerContext,
    ) -> auth_pb2.AccountResponse:
        logging.info("AccountAuthService: AccountRegistration")

        v = DataVerification(grpc_context=context)

        date_config = DateTimeConfig(
            min_datetime=datetime.now() - timedelta(days=120 * 365),
            max_datetime=datetime.now() - timedelta(days=12 * 365),
        )

        date_of_birth = request.date_of_birth.ToDatetime()

        v.verify_string(request.email, "Email", EMAIL_CONFIG)
        v.verify_string(request.password, "Password", PASSWORD_CONFIG)
        v.verify_string(request.first_name, "First name", FIRST_NAME_CONFIG)
        v.verify_string(request.last_name, "Last name", LAST_NAME_CONFIG)
        v.verify_datetime(date_of_birth, "Date of birth", date_config)
        gender = v.convert_enums(request.gender, "Gender", GENDER_ENUM_MAPPING)

        status_mapper = PythonGRPCMapping.mapped(
            ACCOUNT_STATUS_MAPPING, context=context
        )

        with get_db_gen() as db:
            try:
                email_used = (
                    db.query(AccountModel)
                    .filter(AccountModel.email == request.email)
                    .one_or_none()
                )

                if email_used:
                    context.abort(StatusCode.ALREADY_EXISTS, "Email already in use")

                role_id = (
                    db.query(RoleModel.id)
                    .filter(RoleModel.name == AccountRoleEnum.CUSTOMER.value)
                    .one()
                )[0]

                new_account = AccountModel(
                    email=request.email,
                    password=request.password,
                    first_name=request.first_name,
                    last_name=request.last_name,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    email_verified=False,
                    user_status=AccountStatusEnum.UNVERIFIED,
                    role_id=role_id,
                )

                db.add(new_account)
                db.commit()
                db.refresh(new_account)

                return auth_pb2.AccountResponse(
                    id=str(new_account.id),
                    role_id=str(new_account.role_id),
                    first_name=new_account.first_name,
                    last_name=new_account.last_name,
                    verified=new_account.email_verified,
                    master_user=new_account.master_user,
                    user_status=status_mapper.get_alternate_enum(
                        new_account.user_status
                    ),
                )

            except NoResultFound:
                logging.error("Unable to find customer role")
                logging.error("Cancelled account registration")

                context.abort(StatusCode.DATA_LOSS, "Unable to register account")

            except Exception as e:
                logging.exception(e)

                context.abort(StatusCode.UNKNOWN, "Unable to register account")

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
            user_status=AccountStatusEnum.ACTIVE,
        )
