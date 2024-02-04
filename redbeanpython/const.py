import os
from datetime import date
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TypeVar

from redbeanpython.bean.id import Id

TYPE = TypeVar("TYPE", bound=Id | bool | int | float | Decimal | datetime | date | str | bytes | bytearray | None)
ID_TYPE = TypeVar("ID_TYPE", bound=Id | str)

ID = "id"
MODULE_NAME = "redbean"

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


class RebBeanType(Enum):
    ID = "id"
    BOOLEAN = "bool"
    INTEGER = "int"
    FLOAT = "float"
    DECIMAL = "decimal"
    DATETIME = "datetime"
    DATE = "date"
    STRING = "str"
    BYTES = "bytes"
