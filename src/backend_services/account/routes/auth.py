import logging

from argon2 import PasswordHasher
from datetime import datetime, timedelta
from grpc import ServicerContext, StatusCode
from sqlalchemy.exc import NoResultFound
from typing import Self

from utils.proto.account import auth_pb2, auth_pb2_grpc
from account.common.utils import get_db_gen, ACCOUNT_STATUS_MAPPING, GENDER_ENUM_MAPPING
from account.models import AccountModel
from account.services import AuthService, RoleService

from utils.constants import (
    EMAIL_CONFIG,
    FIRST_NAME_CONFIG,
    LAST_NAME_CONFIG,
    PASSWORD_CONFIG,
)
from utils.data_verification import DataVerification
from utils.enums import AccountRoleEnum, AccountStatusEnum
from utils.mapping import EnumMapping
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

        gender_mapper = EnumMapping.mapped(GENDER_ENUM_MAPPING, context=context)
        status_mapper = EnumMapping.mapped(ACCOUNT_STATUS_MAPPING, context=context)

        db_gen = get_db_gen()
        db = next(db_gen)

        auth_service = AuthService(db)
        role_service = RoleService(db)

        try:
            if auth_service.is_email_used(request.email):
                context.abort(StatusCode.ALREADY_EXISTS, "Email already in use")

            role = role_service.get_by_name(AccountRoleEnum.CUSTOMER.value)

            new_account = AccountModel(
                email=request.email,
                password=request.password,
                first_name=request.first_name,
                last_name=request.last_name,
                date_of_birth=date_of_birth,
                gender=gender_mapper.get_alternate_enum(request.gender),
                email_verified=False,
                user_status=AccountStatusEnum.UNVERIFIED,
                role_id=role.id,
            )

            auth_service.add(new_account)
            db.commit()

            return auth_pb2.AccountResponse(
                id=str(new_account.id),
                role_id=str(new_account.role_id),
                first_name=new_account.first_name,
                last_name=new_account.last_name,
                verified=new_account.email_verified,
                master_user=new_account.master_user,
                user_status=status_mapper.get_alternate_enum(new_account.user_status),
            )

        except LookupError:
            logging.error("Unable to find customer role")
            logging.error("Cancelled account registration")

            context.abort(StatusCode.DATA_LOSS, "Unable to register account")

        except Exception as e:
            logging.exception(e)

            context.abort(StatusCode.UNKNOWN, "Unable to register account")

        finally:
            db_gen.close()

    def AccountLogin(
        self: Self, request: auth_pb2.AccountLoginRequest, context: ServicerContext
    ) -> auth_pb2.AccountResponse:
        logging.info("AccountAuthService: AccountLogin")

        v = DataVerification(grpc_context=context)

        v.verify_string(request.email, "Email", EMAIL_CONFIG)
        v.verify_string(request.password, "Password", PASSWORD_CONFIG)

        status_mapper = EnumMapping.mapped(ACCOUNT_STATUS_MAPPING, context=context)

        db_gen = get_db_gen()
        db = next(db_gen)

        try:
            account = (
                db.query(AccountModel).filter(AccountModel.email == request.email).one()
            )

            if not PasswordHasher().verify(account.password, request.password):
                raise ValueError("Password does not match")

            return auth_pb2.AccountResponse(
                id=str(account.id),
                role_id=str(account.role_id),
                first_name=account.first_name,
                last_name=account.last_name,
                verified=account.email_verified,
                master_user=account.master_user,
                user_status=status_mapper.get_alternate_enum(account.user_status),
            )

        except (NoResultFound, ValueError):
            logging.error("Unable to find account")
            logging.error("Cancelled account login")

            context.abort(StatusCode.NOT_FOUND, "Email or password incorrect")

        except Exception as e:
            logging.exception(e)

            context.abort(StatusCode.UNKNOWN, "Unable to log into account")

        finally:
            db_gen.close()
