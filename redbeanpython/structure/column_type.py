from dataclasses import dataclass
from typing import Self
from typing import Type


@dataclass()
class ColumnType:
    alchemy_type: str
    alchemy_definition: str
    sql_column_types: list[str]
    type: Type
    name: str | None = None

    def match_value(self, name: str, value: Type) -> bool:
        return isinstance(value, self.type) and (self.name == name or self.name is None)

    def match_sql_column(self, column_name: str, column_type: str) -> bool:
        if column_name == self.name:
            return True
        column_type = column_type.split("(")[0].lower()
        return column_type in self.sql_column_types

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.type == other.type and self.alchemy_type == other.alchemy_type

