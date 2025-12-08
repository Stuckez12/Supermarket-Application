from utils.enums import TriBool
from utils.schemas.data_verification import StringConfig


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
