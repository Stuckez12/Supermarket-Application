from pydantic import BaseModel


class DatabaseURL(BaseModel):
    username: str
    password: str
    host: str
    port: int
    db_name: str

    def __str__(self):
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class DatabaseSettings(BaseModel):
    pool_pre_ping: bool = True
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 1800
