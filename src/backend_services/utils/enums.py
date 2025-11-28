from enum import Enum


class TriBool(Enum):
    TRUE = True
    FALSE = False
    NONE = None

    def __new__(cls, value=None):
        if value is None:
            value = None

        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    @classmethod
    def _missing_(cls, _):
        return cls.NONE
