from types import NoneType
from typing import Self

from sqlalchemy import inspect

from redbeanpython.bean.bean import Bean
from redbeanpython.const import TYPE
from redbeanpython.errors import TypeChangeError
from redbeanpython.model.model import Model
from redbeanpython.structure.column_type import ColumnType
from redbeanpython.structure.type import TypeFactory


class TableDefinition:
    def __init__(self, name: str, columns: dict[str, ColumnType]):
        self._name = name
        self._columns = columns

    @classmethod
    def from_model_class(cls, bean_name: str, model: type[Model]) -> Self:
        columns = {}
        for attr_name in [ca.key for ca in inspect(model).mapper.column_attrs]:
            type_definition = TypeFactory.from_sql(
                column_name=attr_name,
                column_type=str(getattr(model, str(attr_name)).type),
            )
            columns[attr_name] = type_definition
        return cls(bean_name, columns)

    @property
    def name(self):
        return self._name

    @property
    def columns(self) -> dict[str, ColumnType]:
        return dict(sorted(self._columns.items()))

    @classmethod
    def extend(cls, current_definition: Self | None, bean: Bean):
        columns = current_definition.columns.copy() if current_definition else {}
        for key, value in dict(bean).items():
            if isinstance(value, NoneType):
                continue
            new_type = TypeFactory.from_value(key, value)
            if key not in columns:
                columns[key] = new_type

            if value and columns[key] != new_type:
                raise TypeChangeError(
                    f"Column {key} has different type: {columns[key]} != {new_type}. "
                    f"If you want to alter type change corresponding model definition."
                )
        return TableDefinition(bean.bean_type, columns)

    def __eq__(self, other: TYPE):
        if not isinstance(other, type(self)):
            return False
        if self.name != other.name:
            return False
        if len(self.columns) != len(other.columns):
            return False
        return self.columns == other.columns

    def get_properties_dict(self) -> dict[str, TYPE]:
        return {name: None for name in self.columns.keys()}
