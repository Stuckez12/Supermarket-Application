from grpc import ServicerContext, StatusCode
from typing import Any, Self


class EnumMapping:
    def __init__(
        self: Self, mappings: dict, context: ServicerContext | None = None
    ) -> None:
        self.grpc_context = context
        self.mapping = mappings

    @classmethod
    def mapped(
        cls: type[Self], mappings: dict, context: ServicerContext | None = None
    ) -> Self:
        mapping = {}

        for key, value in mappings.items():
            mapping[key] = value
            mapping[value] = key

        return cls(mapping, context)

    # TODO: Complete this func
    @classmethod
    def named(cls, enum_1: Any, enum_2: Any, context: ServicerContext | None = None):
        assert len(enum_1) == len(enum_2), "Both enums must be the same length"

        mapping: dict = {}

        return cls(mapping, context)

    def get_alternate_enum(self, enum: Any):
        try:
            return self.mapping.get(enum)

        except:
            if self.grpc_context:
                self.grpc_context.abort(
                    StatusCode.NOT_FOUND, f"Alternate enum does not exist for {enum}"
                )

            raise ValueError(f"Alternate enum does not exist for {enum}")
