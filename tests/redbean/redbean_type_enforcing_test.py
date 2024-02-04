from datetime import date
from datetime import datetime
from decimal import Decimal

import pytest

from redbeanpython.errors import TypeChangeError
from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanTypesOperations(RedBeanTestAbstract):
    def test_type_should_be_locked(self):
        rb = self.get_red_bean()
        bean = rb.dispense(self.BEAN_TYPE)
        bean.a = 123
        bean["b"] = "abc"
        rb.store(bean)

        bean.a = 456
        bean["b"] = "xyz"
        rb.store(bean)

        with pytest.raises(TypeChangeError):
            bean.a = "abc"
            rb.store(bean)

        with pytest.raises(TypeChangeError):
            bean["b"] = 123
            rb.store(bean)

        assert rb.load(self.BEAN_TYPE, bean.id).a == 456
        assert rb.load(self.BEAN_TYPE, bean.id)["b"] == "xyz"

        bean.a = None
        bean["b"] = None
        rb.store(bean)

        assert rb.load(self.BEAN_TYPE, bean.id).a is None
        assert rb.load(self.BEAN_TYPE, bean.id)["b"] is None

    def test_type_enforcing(self):
        rb = self.get_red_bean()
        bean = rb.dispense(self.BEAN_TYPE)
        bean.int = 123
        bean.bool = True
        bean.str = "abc"
        bean.float = 1.1
        bean.datetime = datetime.fromisoformat("2021-01-01 00:00:00")
        bean.date = date.fromisoformat("2021-03-03")
        bean.bytes = b"123"
        bean.decimal = Decimal("10.1")

        rb.store(bean)

        assert rb.load(self.BEAN_TYPE, bean.id).int == 123
        assert rb.load(self.BEAN_TYPE, bean.id).bool is True
        assert rb.load(self.BEAN_TYPE, bean.id).str == "abc"
        assert rb.load(self.BEAN_TYPE, bean.id).float == 1.1
        assert rb.load(self.BEAN_TYPE, bean.id).datetime == datetime.fromisoformat(
            "2021-01-01 00:00:00"
        )
        assert rb.load(self.BEAN_TYPE, bean.id).date == date.fromisoformat("2021-03-03")
        assert rb.load(self.BEAN_TYPE, bean.id).bytes == b"123"
        assert rb.load(self.BEAN_TYPE, bean.id).decimal == Decimal("10.1")

        bean.int = None
        bean.bool = None
        bean.float = None
        bean.str = None
        bean.datetime = None
        bean.date = None
        bean.bytes = None
        bean.decimal = None
        rb.store(bean)

        assert rb.load(self.BEAN_TYPE, bean.id).int is None
        assert rb.load(self.BEAN_TYPE, bean.id).bool is None
        assert rb.load(self.BEAN_TYPE, bean.id).float is None
        assert rb.load(self.BEAN_TYPE, bean.id).str is None
        assert rb.load(self.BEAN_TYPE, bean.id).datetime is None
        assert rb.load(self.BEAN_TYPE, bean.id).date is None
        assert rb.load(self.BEAN_TYPE, bean.id).bytes is None
        assert rb.load(self.BEAN_TYPE, bean.id).decimal is None

        bean = rb.load(self.BEAN_TYPE, bean.id)
        bean.int = 1
        bean.bool = False
        bean.float = 2.2
        bean.str = "vvv"
        bean.datetime = datetime.fromisoformat("2021-11-11 00:00:01")
        bean.date = date.fromisoformat("2021-12-12")
        bean.bytes = b"new"
        bean.decimal = Decimal("1000.1")
        rb.store(bean)

        with pytest.raises(TypeChangeError):
            bean.int = "abc"
            rb.store(bean)
        with pytest.raises(TypeChangeError):
            bean.bool = 1.1
            rb.store(bean)
        with pytest.raises(TypeChangeError):
            bean.float = False
            rb.store(bean)
        with pytest.raises(TypeChangeError):
            bean.str = 123
            rb.store(bean)
        with pytest.raises(TypeChangeError):
            bean.datetime = 123
            rb.store(bean)
        with pytest.raises(TypeChangeError):
            bean.date = 123
            rb.store(bean)
        with pytest.raises(TypeChangeError):
            bean.bytes = "str"
            rb.store(bean)
        with pytest.raises(TypeChangeError):
            bean.decimal = 1
            rb.store(bean)

        assert rb.load(self.BEAN_TYPE, bean.id).int == 1
        assert rb.load(self.BEAN_TYPE, bean.id).bool is False
        assert rb.load(self.BEAN_TYPE, bean.id).float == 2.2
        assert rb.load(self.BEAN_TYPE, bean.id).str == "vvv"
        assert rb.load(self.BEAN_TYPE, bean.id).datetime == datetime.fromisoformat(
            "2021-11-11 00:00:01"
        )
        assert rb.load(self.BEAN_TYPE, bean.id).date == date.fromisoformat("2021-12-12")
        assert rb.load(self.BEAN_TYPE, bean.id).bytes == b"new"
        assert rb.load(self.BEAN_TYPE, bean.id).decimal == Decimal("1000.1")

    def test_type_enforcing_with_null(self):
        rb = self.get_red_bean()
        bean = rb.dispense(self.BEAN_TYPE)
        bean.a = 123
        rb.store(bean)

        assert rb.load(self.BEAN_TYPE, bean.id).a == 123

        with pytest.raises(TypeChangeError):
            bean.a = "100"
            rb.store(bean)
        assert rb.load(self.BEAN_TYPE, bean.id).a == 123

        bean.a = None
        rb.store(bean)
        assert rb.load(self.BEAN_TYPE, bean.id).a is None

        with pytest.raises(TypeChangeError):
            bean.a = "100"
            rb.store(bean)
        assert rb.load(self.BEAN_TYPE, bean.id).a is None
