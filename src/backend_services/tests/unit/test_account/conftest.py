import pytest

from alembic import command
from alembic.config import Config
from argon2 import PasswordHasher
from datetime import datetime
from sqlalchemy.orm import Session

from account.common.utils.seed_db import seed_db
from account.models import AccountModel, RoleModel
from account.settings import settings
from account.services import AuthService

from utils.database import get_db, db_connection, get_database_url
from utils.enums import AccountRoleEnum, AccountStatusEnum, GenderEnum
from utils.schemas import DatabaseSettings


# ========================================================================== #
# -------------------------------- DATABASE -------------------------------- #
# ========================================================================== #


TEST_DB_URL_OBJ = settings.get_db_url()
TEST_DB_URL_OBJ.db_name = "account"

TEST_DB_SETTINGS = DatabaseSettings(
    pool_pre_ping=True,
    pool_size=4,
    max_overflow=4,
    pool_timeout=30,
    pool_recycle=300,
)


@pytest.fixture(scope="session", autouse=True)
def migrate_db():
    alembic_cfg = Config("src/backend_services/account/alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", get_database_url(TEST_DB_URL_OBJ))
    command.upgrade(alembic_cfg, "head")

    seed_db()

    yield

    command.downgrade(alembic_cfg, "base")


@pytest.fixture
def db_conn():
    yield db_connection(TEST_DB_URL_OBJ, TEST_DB_SETTINGS)


@pytest.fixture
def db_generator(db_conn):
    yield get_db(db_conn)


@pytest.fixture
def session(db_generator):
    yield next(db_generator)


# ========================================================================== #
# -------------------------------- SERVICES -------------------------------- #
# ========================================================================== #


@pytest.fixture
def auth_service(session):
    yield AuthService(session)


# ========================================================================== #
# ------------------------------- TEST DATA -------------------------------- #
# ========================================================================== #


@pytest.fixture
def test_customer(session: Session):
    role = (
        session.query(RoleModel)
        .filter(RoleModel.name == AccountRoleEnum.CUSTOMER.value)
        .one()
    )

    user = AccountModel(
        email="test@customer.com",
        password=PasswordHasher().hash("Password1."),
        first_name="Test",
        last_name="Account",
        date_of_birth=datetime.now(),
        gender=GenderEnum.MALE,
        email_verified=True,
        user_status=AccountStatusEnum.ACTIVE,
        role_id=role.id,
        password_last_changed_at=None,
        failed_login_attempts=0,
        account_locked_until=None,
        last_login=None,
        master_user=False,
    )

    session.add(user)
    session.commit()

    yield user

    session.delete(user)
    session.commit()
