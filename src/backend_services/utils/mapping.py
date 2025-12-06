import logging

from enum import Enum
from grpc import ServicerContext, StatusCode
from typing import Any, Self


class PythonGRPCMapping:
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
    def named(
        cls: Self, python_enum: Enum, grpc_enum, context: ServicerContext | None = None
    ):
        assert len(python_enum) == len(
            grpc_enum
        ), "Both python and grpc enums must be the same length"

        for name in python_enum:
            logging.info(name)
            logging.info(type(name))

        mapping = {}

        return cls(mapping, context)

    def get_alternate_enum(self, enum: Any):
        try:
            logging.info(enum)
            logging.info(enum)
            logging.info(enum)
            logging.info(enum)
            logging.info(enum)
            return self.mapping.get(enum)

        except:
            if self.grpc_context:
                self.grpc_context.abort(
                    StatusCode.NOT_FOUND, f"Alternate enum does not exist for {enum}"
                )

            raise ValueError(f"Alternate enum does not exist for {enum}")
