from pydantic import BaseModel


class DatabaseURL(BaseModel):
    username: str
    password: str
    host: str
    port: str
    db_name: str


class DatabaseSettings(BaseModel):
    pool_pre_ping: bool = True
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 1800
