import re
from datetime import date
from datetime import datetime
from decimal import Decimal
from types import NoneType

from redbeanpython.const import TYPE
from redbeanpython.errors import IncorrectNameError
from redbeanpython.errors import IncorrectValueError


class NameValidator:
    @classmethod
    def validate_property_name(cls, name: TYPE) -> None:
        cls._validate(name, "Property name")
        if name == "keys":
            raise IncorrectNameError(f"Property name can not be restricted keyword: {name}")

    @classmethod
    def validate_bean_type(cls, bean_type: TYPE) -> None:
        cls._validate(bean_type, "Bean")

    @staticmethod
    def _validate(value: TYPE, type_: str) -> None:
        if not isinstance(value, str):
            raise IncorrectNameError(f"{type_} must be string, not {type(value)}")
        if value.strip() == "":
            raise IncorrectNameError(f"{type_} must not be empty, not {value}")
        if value.startswith("_"):
            raise IncorrectNameError(f"{type_} must not start with underscore")
        if not re.match(r"^[a-z_][0-9a-z_]*$", value):
            raise IncorrectNameError(f"{type_} must be correct identifier, not {value}")


class ValueValidator:
    @staticmethod
    def validate(value: TYPE) -> None:
        if not isinstance(value, (str, bool, int, float, Decimal, datetime, date, bytes, bytearray, NoneType)):
            raise IncorrectValueError(f"Unsupported type: {type(value)}")
        if isinstance(value, datetime) and value.tzinfo is not None:
            raise IncorrectValueError(f"datetime must not have timezone: {value}")
