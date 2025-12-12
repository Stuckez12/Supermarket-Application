import grpc
import logging

from concurrent import futures

from account.common.utils.seed_db import seed_db
from account.proto import auth_pb2_grpc
from account.routes import AccountAuthService
from account.settings import settings

from utils.app_initialise import Initialise
from utils.services.database import (
    account_db_settings,
    account_db_url_obj,
)


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def add_services(server: grpc.Server) -> None:
    auth_pb2_grpc.add_AccountAuthServiceServicer_to_server(AccountAuthService(), server)
    logging.info("Service added: Account Authentication")


def start_server() -> None:
    logging.info("Beginning external checks")
    logging.info("- Database checks")
    external_checks = Initialise(account_db_url_obj, account_db_settings)

    external_checks.create_database_if_not_exists()
    external_checks.check_database_connection()
    external_checks.initialise_database("api/account/alembic.ini", seed_db)

    logging.info("- Finalising checks")
    external_checks.wrap_up_initialisation()

    logging.info("Initialising server")
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=settings.SERVER_MAX_WORKERS)
    )

    server_credentials = grpc.ssl_server_credentials(
        [
            (
                open("/api/certificates/private_key/account.pem", "rb").read(),
                open("/api/certificates/certificate/account.pem", "rb").read(),
            )
        ]
    )

    logging.info("Creating secure gRPC port")
    server.add_secure_port(f"[::]:{settings.SERVER_PORT}", server_credentials)

    logging.info("Adding all gRPC services")
    add_services(server)

    logging.info(
        f"Starting gRPC server on https://{settings.SERVER_HOST}:{settings.SERVER_PORT}"
    )
    server.start()
    logging.info("Server is now ready")

    server.wait_for_termination()


if __name__ == "__main__":
    start_server()
