from redbeanpython.const import TYPE
from redbeanpython.structure.column_type import ColumnType
from redbeanpython.structure.supported_types import SUPPORTED_TYPES


class TypeFactory:
    @classmethod
    def from_value(cls, name: str, value: TYPE) -> ColumnType:
        for type_enum, column_type in SUPPORTED_TYPES.items():
            if column_type.match_value(name=name, value=value):
                return SUPPORTED_TYPES[type_enum]
        raise NotImplementedError(f"Type {type(value)} is not supported.")

    @classmethod
    def from_sql(cls, column_name: str, column_type: str) -> ColumnType:
        for type_enum, column in SUPPORTED_TYPES.items():
            if column.match_sql_column(column_name=column_name, column_type=column_type):
                return SUPPORTED_TYPES[type_enum]
        raise NotImplementedError(f"Type {column_type} is not supported.")
