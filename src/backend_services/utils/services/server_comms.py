import grpc
import logging
import time

from google.protobuf.message import Message
from grpc import RpcError, StatusCode
from typing import Callable, Generic, TypeVar

from utils.constants import GRPC_CHANNEL_OPTIONS


REQUEST_MESSAGE = TypeVar("REQUEST_MESSAGE", bound=Message)
RESPONSE_MESSAGE = TypeVar("RESPONSE_MESSAGE", bound=Message)
REQUESTS = TypeVar("REQUESTS")
STUBS = TypeVar("STUBS")


class ServerCommunication(Generic[RESPONSE_MESSAGE]):
    def __init__(
        self,
        channel_host: str,
        channel_port: int,
        channel_secure: bool = False,
        server_certificate: str | None = None,
        rpc_max_retries: int = 3,
        channel_options: list = GRPC_CHANNEL_OPTIONS,
    ) -> None:

        self.host = channel_host
        self.port = channel_port

        self.stub = None

        self.secure_channel = channel_secure
        self.certificate = None

        self.options = channel_options
        self.max_retries = rpc_max_retries

        if self.secure_channel:
            if server_certificate is None:
                error_msg = f"Failed to initialise ServerCommunication for '{self.host}:{self.port}'. Server certificate must be provided"

                raise AttributeError(error_msg)

            else:
                credentials = open(server_certificate, "rb").read()
                self.certificate = grpc.ssl_channel_credentials(
                    root_certificates=credentials
                )

        self._reconnect()

    def _reconnect(self) -> None:
        url = f"{self.host}:{self.port}"

        if self.secure_channel:
            self.channel = grpc.secure_channel(
                url, self.certificate, options=self.options  # type: ignore[arg-type]
            )

        else:
            self.channel = grpc.insecure_channel(url, options=self.options)

    def _retry(self, attempt_count: int) -> None:
        time.sleep(2**attempt_count)

    def oto_request(
        self,
        request: str,
        stub: Callable[[], STUBS],
        data: REQUEST_MESSAGE,
    ) -> RESPONSE_MESSAGE:
        for attempt in range(self.max_retries):
            try:
                stub_channel = stub(self.channel)  # type: ignore[call-arg]
                func = getattr(stub_channel, request)

                return func(data)

            except RpcError as err:
                status = err.code()
                response = err.details()

                match status:
                    case StatusCode.UNKNOWN:
                        if attempt == self.max_retries - 1:
                            logging.error("Service raised an unknown error")
                            logging.error(response)
                            raise SystemError("Service raised an unknown error")

                        self._retry(attempt)

                    case StatusCode.INTERNAL:
                        logging.error("Service raised an internal error")
                        logging.error(response)
                        raise SystemError("Service raised an internal error")

                    case StatusCode.UNAUTHENTICATED:
                        raise PermissionError(
                            "You must be logged in to perform this action"
                        )

                    case StatusCode.PERMISSION_DENIED:
                        raise PermissionError(
                            "You do not have the required permissions"
                        )

                    case StatusCode.ALREADY_EXISTS:
                        raise ValueError("Data already exists within the system")

                    case StatusCode.DATA_LOSS:
                        logging.error("Data loss has occurred")
                        logging.error(response)
                        raise MemoryError("Unrecoverable data loss has occurred")

                    case StatusCode.INVALID_ARGUMENT:
                        raise ValueError("Invalid parameters provided")

                    case StatusCode.UNAVAILABLE:
                        raise ConnectionError("Service is currently unavailable")

                    case _:
                        self._retry(attempt)

        raise ConnectionError(
            "Unable to receive a valid response from the specified service"
        )
