from copy import deepcopy
from datetime import date
from datetime import datetime
from decimal import Decimal

import pytest

from redbeanpython.const import RebBeanType
from redbeanpython.structure.supported_types import SUPPORTED_TYPES
from redbeanpython.structure.type import TypeFactory
from tests.structure.abstract import StructureTestAbstract


class TestColumnType(StructureTestAbstract):
    def test_alchemy(self):
        for type_, expected in {
            RebBeanType.ID: "String",
            RebBeanType.STRING: "Text",
            RebBeanType.INTEGER: "BigInteger",
            RebBeanType.FLOAT: "Float",
            RebBeanType.DECIMAL: "Numeric",
            RebBeanType.DATETIME: "DateTime",
            RebBeanType.DATE: "Date",
            RebBeanType.BYTES: "LargeBinary",
            RebBeanType.BOOLEAN: "Boolean",
        }.items():
            assert SUPPORTED_TYPES[type_].alchemy_type == expected

        for type_, expected in {
            RebBeanType.ID: "Column(String(255), primary_key=True)",
            RebBeanType.STRING: "Column(Text, nullable=True)",
            RebBeanType.INTEGER: "Column(BigInteger, nullable=True)",
            RebBeanType.FLOAT: "Column(Float, nullable=True)",
            RebBeanType.DECIMAL: "Column(Numeric(precision=30, scale=10), nullable=True)",
            RebBeanType.DATETIME: "Column(DateTime, nullable=True)",
            RebBeanType.DATE: "Column(Date, nullable=True)",
            RebBeanType.BYTES: "Column(LargeBinary, nullable=True)",
            RebBeanType.BOOLEAN: "Column(Boolean, nullable=True)",
        }.items():
            assert SUPPORTED_TYPES[type_].alchemy_definition == expected

        with pytest.raises(NotImplementedError):
            _ = TypeFactory.from_value(name="any", value={})

        with pytest.raises(NotImplementedError):
            _ = TypeFactory.from_sql(column_name="any", column_type="unknown")

    def test_from_value(self):
        assert TypeFactory.from_value("id", "123") == SUPPORTED_TYPES[RebBeanType.ID]
        assert TypeFactory.from_value("x", "a") == SUPPORTED_TYPES[RebBeanType.STRING]
        assert TypeFactory.from_value("x", 123) == SUPPORTED_TYPES[RebBeanType.INTEGER]
        assert TypeFactory.from_value("x", 1.1) == SUPPORTED_TYPES[RebBeanType.FLOAT]
        assert (
            TypeFactory.from_value("x", Decimal("1.1"))
            == SUPPORTED_TYPES[RebBeanType.DECIMAL]
        )
        assert (
            TypeFactory.from_value("x", datetime.now())
            == SUPPORTED_TYPES[RebBeanType.DATETIME]
        )
        assert (
            TypeFactory.from_value("x", date.today())
            == SUPPORTED_TYPES[RebBeanType.DATE]
        )
        assert TypeFactory.from_value("x", True) == SUPPORTED_TYPES[RebBeanType.BOOLEAN]

    def test_from_column(self):
        assert TypeFactory.from_sql("id", "any") == SUPPORTED_TYPES[RebBeanType.ID]

        for column_type, expected in {
            "Boolean": SUPPORTED_TYPES[RebBeanType.BOOLEAN],
            "TinyInt": SUPPORTED_TYPES[RebBeanType.BOOLEAN],
            "Integer": SUPPORTED_TYPES[RebBeanType.INTEGER],
            "BigInt": SUPPORTED_TYPES[RebBeanType.INTEGER],
            "Float": SUPPORTED_TYPES[RebBeanType.FLOAT],
            "Double Precision": SUPPORTED_TYPES[RebBeanType.FLOAT],
            "Numeric(20,10)": SUPPORTED_TYPES[RebBeanType.DECIMAL],
            "Decimal(20,10)": SUPPORTED_TYPES[RebBeanType.DECIMAL],
            "Datetime": SUPPORTED_TYPES[RebBeanType.DATETIME],
            "TIMESTAMP": SUPPORTED_TYPES[RebBeanType.DATETIME],
            "Date": SUPPORTED_TYPES[RebBeanType.DATE],
            "largebinary": SUPPORTED_TYPES[RebBeanType.BYTES],
            "Bytes": SUPPORTED_TYPES[RebBeanType.BYTES],
            "BLOB": SUPPORTED_TYPES[RebBeanType.BYTES],
            "Bytea": SUPPORTED_TYPES[RebBeanType.BYTES],
            "Text": SUPPORTED_TYPES[RebBeanType.STRING],
        }.items():
            assert TypeFactory.from_sql("any", column_type) == expected

    def test_equality(self):
        assert SUPPORTED_TYPES[RebBeanType.ID] != "other"
        assert SUPPORTED_TYPES[RebBeanType.ID] == SUPPORTED_TYPES[RebBeanType.ID]
        assert SUPPORTED_TYPES[RebBeanType.ID] == deepcopy(SUPPORTED_TYPES[RebBeanType.ID])
        assert SUPPORTED_TYPES[RebBeanType.ID] != SUPPORTED_TYPES[RebBeanType.STRING]

