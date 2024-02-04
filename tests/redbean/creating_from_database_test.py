from datetime import date, datetime
from decimal import Decimal

from redbeanpython import Bean
from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanCreatingFromDatabase(RedBeanTestAbstract):
    def test_act_on_empty_db(self):
        rb = self.get_red_bean()

        bean = rb.load("test", "1234")
        assert bean.id == "1234"
        assert "name" not in bean
        assert bean.name is None

    def test_act_on_not_empty_database(self):
        rb = self.get_red_bean()

        content = {
            f"bool_1": True,
            f"int_1": 123,
            f"string_1": f"any_1",
            f"float_1": 1.1,
            f"decimal_1": Decimal("123.123"),
            f"datetime_1": datetime.fromisoformat(f"2001-01-01 00:00:00"),
            f"date_1": date.fromisoformat(f"2002-01-01"),
            f"bytes": b"123",
        }
        first_bean_id = rb.store(Bean(self.BEAN_TYPE, content))

        bean = rb.load(self.BEAN_TYPE, "1234")
        assert bean.id == "1234"
        assert "string_1" in bean
        assert bean.string_1 is None

        bean = rb.load(self.BEAN_TYPE, first_bean_id)

        assert bean["bool_1"] is True
        assert isinstance(bean["bool_1"], bool)

        assert bean["int_1"] == 123
        assert isinstance(bean["int_1"], int)

        assert bean["string_1"] == "any_1"
        assert isinstance(bean["string_1"], str)

        assert round(bean["float_1"], 1) == round(1.1, 1)
        assert isinstance(bean["float_1"], float)

        assert bean["decimal_1"] == Decimal("123.123")
        assert isinstance(bean["decimal_1"], Decimal)

        assert bean["datetime_1"] == datetime.fromisoformat("2001-01-01 00:00:00")
        assert isinstance(bean["datetime_1"], datetime)
        assert bean["datetime_1"].tzinfo is None

        assert bean["date_1"] == datetime.fromisoformat("2002-01-01").date()
        assert isinstance(bean["date_1"], date)
        assert not isinstance(bean["date_1"], datetime)

        assert bean["bytes"] == b"123"
        assert isinstance(bean["bytes"], bytes)
