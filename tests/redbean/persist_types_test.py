import os
from datetime import date, datetime
from decimal import Decimal

from redbeanpython import Bean
from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanExists(RedBeanTestAbstract):
    def test_types_are_correctly_persisted(self):
        rb = self.get_red_bean()
        max_decimal = Decimal(f"{'1' * 20}.{'5' * 10}")
        if os.environ.get("DB_TYPE") == "sqlite":
            max_decimal = Decimal(f"{'1' * 5}.{'5' * 5}")
        max_int = 2_147_483_647 * 1000_000
        content = {
            "id": "id_overriden",
            "bool_1": True,
            "int_1": max_int,
            "string_1": f"any_1",
            "float_1": 1.1,
            "decimal_1": max_decimal,
            "datetime_1": datetime.fromisoformat(f"2001-01-01 00:00:00"),
            "date_1": date.fromisoformat(f"2002-01-01"),
            "bytes": b"123",
        }

        bean_id = rb.store(Bean(self.BEAN_TYPE, content))

        bean = rb.load(self.BEAN_TYPE, bean_id=bean_id)

        assert bean["id"] == "id_overriden"
        assert isinstance(bean["id"], str)

        assert bean["bool_1"] is True
        assert isinstance(bean["bool_1"], bool)

        assert bean["int_1"] == max_int
        assert isinstance(bean["int_1"], int)

        assert bean["string_1"] == "any_1"
        assert isinstance(bean["string_1"], str)

        assert round(bean["float_1"], 1) == round(1.1, 1)
        assert isinstance(bean["float_1"], float)

        assert bean["decimal_1"] == max_decimal
        assert isinstance(bean["decimal_1"], Decimal)

        assert bean["datetime_1"] == datetime.fromisoformat("2001-01-01 00:00:00")
        assert isinstance(bean["datetime_1"], datetime)
        assert bean["datetime_1"].tzinfo is None

        assert bean["date_1"] == datetime.fromisoformat("2002-01-01").date()
        assert isinstance(bean["date_1"], date)
        assert not isinstance(bean["date_1"], datetime)

        assert bean["bytes"] == b"123"
        assert isinstance(bean["bytes"], bytes)
