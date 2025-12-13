from pydantic import BaseModel

from utils.enums.enums import AccountRoleEnum


class RoleMappingSchema(BaseModel):
    name: AccountRoleEnum
    description: str
