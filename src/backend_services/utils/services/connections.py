import os

from utils.proto.server_comms import ServerCommunication


account_connection = ServerCommunication(
    channel_host=os.environ.get("ACCOUNT_SERVICE_HOST", "localhost"),
    channel_port=os.environ.get("ACCOUNT_SERVICE_PORT", 50050),
    channel_secure=True,
    server_certificate="/api/certificates/certificate/account.pem",
    rpc_max_retries=5,
)
