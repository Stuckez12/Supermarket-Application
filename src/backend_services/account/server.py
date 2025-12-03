import grpc
import logging

from concurrent import futures

from account.proto import auth_pb2_grpc
from account.routes import AccountAuthService
from account.settings import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


def add_services(server: grpc.Server) -> None:
    auth_pb2_grpc.add_AccountAuthServiceServicer_to_server(AccountAuthService(), server)
    print("Service Added: User-Authentication")


def start_server() -> None:
    logger.info("Beginning server setup")
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

    server.add_secure_port(f"[::]:{settings.SERVER_PORT}", server_credentials)
    logger.info(
        f"Starting gRPC server on https://{settings.SERVER_HOST}:{settings.SERVER_PORT}"
    )

    server.start()
    logger.info("Server is running. Beginning server setup")

    add_services(server)

    logger.info("Server is now ready")
    server.wait_for_termination()


if __name__ == "__main__":
    start_server()
