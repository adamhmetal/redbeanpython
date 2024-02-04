from datetime import date
from datetime import datetime
from decimal import Decimal

from redbeanpython.const import RebBeanType
from redbeanpython.structure.column_type import ColumnType

SUPPORTED_TYPES: dict[RebBeanType, ColumnType] = {
    RebBeanType.ID: ColumnType(
        alchemy_type="String",
        alchemy_definition="Column(String(255), primary_key=True)",
        sql_column_types=["varchar"],
        type=str,
        name="id",
    ),
    RebBeanType.BOOLEAN: ColumnType(
        alchemy_type="Boolean",
        alchemy_definition="Column(Boolean, nullable=True)",
        sql_column_types=["boolean", "tinyint"],
        type=bool,
    ),
    RebBeanType.INTEGER: ColumnType(
        alchemy_type="BigInteger",
        alchemy_definition="Column(BigInteger, nullable=True)",
        sql_column_types=["integer", "bigint"],
        type=int,
    ),
    RebBeanType.FLOAT: ColumnType(
        alchemy_type="Float",
        alchemy_definition="Column(Float, nullable=True)",
        sql_column_types=["float", "double precision"],
        type=float,
    ),
    RebBeanType.DECIMAL: ColumnType(
        alchemy_type="Numeric",
        alchemy_definition="Column(Numeric(precision=30, scale=10), nullable=True)",
        sql_column_types=["numeric", "decimal"],
        type=Decimal,
    ),
    RebBeanType.DATETIME: ColumnType(
        alchemy_type="DateTime",
        alchemy_definition="Column(DateTime, nullable=True)",
        sql_column_types=["datetime", "timestamp"],
        type=datetime,
    ),
    RebBeanType.DATE: ColumnType(
        alchemy_type="Date",
        alchemy_definition="Column(Date, nullable=True)",
        sql_column_types=["date"],
        type=date,
    ),
    RebBeanType.BYTES: ColumnType(
        alchemy_type="LargeBinary",
        alchemy_definition="Column(LargeBinary, nullable=True)",
        sql_column_types=["largebinary", "bytes", "blob", "bytea"],
        type=bytes,
    ),
    RebBeanType.STRING: ColumnType(
        alchemy_type="Text",
        alchemy_definition="Column(Text, nullable=True)",
        sql_column_types=["text"],
        type=str,
    ),
}
