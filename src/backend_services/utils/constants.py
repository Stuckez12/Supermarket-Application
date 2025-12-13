from utils.enums.enums import TriBool
from utils.schemas.data_verification import StringConfig


GRPC_CHANNEL_OPTIONS = [
    # Defines the maximum data size of data one RPC
    # call can send to a server.
    # Data is in bytes (default - 10MB)
    ("grpc.max_send_message_length", 10000000),
    # Defines the maximum data size of data one RPC
    # call can recieve from a response.
    # Data is in bytes (default - 10MB)
    ("grpc.max_receive_message_length", 10000000),
    # Defines how long the connection lasts between
    # the two servers before disconnecting (saves resources).
    # Time is in milliseconds (default - 60 seconds)
    ("grpc.max_connection_idle_ms", 60000),
    # Whether to allow keepalive pings when
    # there are no active RPC calls.
    # (default - 1 (True))
    ("grpc.keepalive_permit_without_calls", 1),
    # Periodically pings the server every interval
    # keeping the connection alive
    # Time is in milliseconds (default - 5 seconds)
    ("grpc.keepalive_time_ms", 5000),
    # Forces the client to wait x time until sending another
    # ping top the connected server.
    # This prevents the client from sending ping more
    # frequently than needed.
    # Time is in milliseconds (default - 5 seconds)
    ("grpc.http2.min_time_between_pings_ms", 5000),
    # How long to wait for a response from the last ping.
    # If no response then the connection is terminated.
    # Time is in milliseconds (default - 2 seconds)
    ("grpc.keepalive_timeout_ms", 2000),
    # Defines how many consecutive pings to send before
    # adding a strike to the connection.
    # This only happens when there has been
    # no RPC calls that return data.
    # (default - 12 inactive pings before a strike)
    ("grpc.http2.max_pings_without_data", 12),
    # Defines how many strikes are allowed to accumulate
    # before terminating the connection.
    # Strikes are permanent until termination and reconnection.
    # (default - 3 strikes)
    ("grpc.http2.max_ping_strikes", 3),
    # Defines the initial backoff time before attempting to reconnect.
    # Time is in milliseconds (default - 0.5 seconds)
    ("grpc.initial_reconnect_backoff_ms", 500),
    # Defines the minimum time between reconnection attempts.
    # Time is in milliseconds (default - 0.5 seconds)
    ("grpc.min_reconnect_backoff_ms", 500),
    # Defines the maximum time between reconnection attempts.
    # Each failed attempt doubles the backoff time until it
    # reaches the specified time below.
    # Time is in milliseconds (default - 4 seconds)
    ("grpc.max_reconnect_backoff_ms", 4000),
]


EMAIL_CONFIG = StringConfig(
    min_len=6,
    max_len=96,
    include_lowercase=TriBool.TRUE,
    include_uppercase=TriBool.NONE,
    include_number=TriBool.NONE,
    include_specials=TriBool.TRUE,
)

PASSWORD_CONFIG = StringConfig(
    min_len=8,
    max_len=256,
    include_lowercase=TriBool.TRUE,
    include_uppercase=TriBool.TRUE,
    include_number=TriBool.TRUE,
    include_specials=TriBool.TRUE,
)

FIRST_NAME_CONFIG = StringConfig(
    min_len=2,
    max_len=64,
    include_lowercase=TriBool.NONE,
    include_uppercase=TriBool.NONE,
    include_number=TriBool.FALSE,
    include_specials=TriBool.FALSE,
)

LAST_NAME_CONFIG = StringConfig(
    min_len=2,
    max_len=64,
    include_lowercase=TriBool.NONE,
    include_uppercase=TriBool.NONE,
    include_number=TriBool.FALSE,
    include_specials=TriBool.NONE,
)
