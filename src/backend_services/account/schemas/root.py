from pydantic import BaseModel


class ApplicationHealth(BaseModel):
    db: bool
