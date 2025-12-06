import grpc
import logging

from concurrent import futures

from account.proto import auth_pb2_grpc
from account.routes import AccountAuthService
from account.settings import settings


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def add_services(server: grpc.Server) -> None:
    auth_pb2_grpc.add_AccountAuthServiceServicer_to_server(AccountAuthService(), server)
    logging.info("Service added: Account Authentication")


def start_server() -> None:
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
