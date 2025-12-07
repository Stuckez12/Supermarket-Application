import pytest

from enum import Enum

from utils.mapping import EnumMapping


class Enum1(Enum):
    VALUE_1 = "1_VALUE_1"
    VALUE_2 = "1_VALUE_2"
    VALUE_3 = "1_VALUE_3"
    VALUE_4 = "1_VALUE_4"
    VALUE_5 = "1_VALUE_5"


class Enum2(Enum):
    VALUE_1 = "2_VALUE_1"
    VALUE_2 = "2_VALUE_2"
    VALUE_3 = "2_VALUE_3"
    VALUE_4 = "2_VALUE_4"
    VALUE_5 = "2_VALUE_5"


class ShortEnum(Enum):
    VALUE_1 = "VALUE_1"
    VALUE_2 = "VALUE_2"
    VALUE_3 = "VALUE_3"


class NumberEnum(Enum):
    NUMBER_1 = "NUMBER_1"
    NUMBER_2 = "NUMBER_2"
    NUMBER_3 = "NUMBER_3"
    NUMBER_4 = "NUMBER_4"
    NUMBER_5 = "NUMBER_5"


class TestEnumMapping:
    @pytest.fixture(scope="class")
    def mapped_enums(self):
        mapped = {
            Enum1.VALUE_1: Enum2.VALUE_1,
            Enum1.VALUE_2: Enum2.VALUE_2,
            Enum1.VALUE_3: Enum2.VALUE_3,
            Enum1.VALUE_4: Enum2.VALUE_4,
            Enum1.VALUE_5: Enum2.VALUE_5,
        }

        return mapped

    def test_mapped_success(self, mapped_enums: dict[Enum1, Enum2]):
        mapping = EnumMapping.mapped(mapped_enums)

        assert type(mapping) == EnumMapping
        assert type(mapping.mapping) == dict
        assert len(mapping.mapping) == len(Enum1) + len(Enum2)

    @pytest.mark.parametrize(
        ("param", "output"),
        [
            (Enum1.VALUE_1, Enum2.VALUE_1),
            (Enum2.VALUE_4, Enum1.VALUE_4),
            (Enum2.VALUE_5, Enum1.VALUE_5),
            (Enum1.VALUE_3, Enum2.VALUE_3),
            (Enum2.VALUE_2, Enum1.VALUE_2),
        ],
    )
    def test_mapped_get_alternate_enum_success(
        self, mapped_enums: dict[Enum1, Enum2], param: Enum, output: Enum
    ):
        mapping = EnumMapping.mapped(mapped_enums)

        assert mapping.get_alternate_enum(param) == output
