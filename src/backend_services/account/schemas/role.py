from pydantic import BaseModel

from utils.enums import AccountRoleEnum


class RoleMappingSchema(BaseModel):
    name: AccountRoleEnum
    description: str
