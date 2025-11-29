from pydantic import BaseModel

from account.common.enums import InteractionType, OperationTags


class PermissionCreateSchema(BaseModel):
    id: str
    name: str
    description: str
    type: InteractionType
    category: str
    tags: list[OperationTags]
    removable: bool = False
