from fastapi import Depends
from typing import Annotated

from utils.services.server_comms import ServerCommunication
from utils.services.connections import account_connection


AccountServiceGRPC = Annotated[ServerCommunication, Depends(lambda: account_connection)]
