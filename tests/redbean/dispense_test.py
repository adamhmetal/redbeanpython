import pytest

from redbeanpython import Beans, IncorrectValueError
from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanDispense(RedBeanTestAbstract):
    def test_replace(self):
        rb = self.get_red_bean()
        bean = rb.dispense(self.BEAN_TYPE)
        bean.a = "a"
        bean.b = "b"
        rb.store(bean)

        bean_id = bean.id

        assert rb.load(self.BEAN_TYPE, bean_id).a == "a"
        assert rb.load(self.BEAN_TYPE, bean_id).b == "b"

        bean = rb.load(self.BEAN_TYPE, bean_id)
        bean.a = "a2"
        rb.store(bean)

        assert rb.load(self.BEAN_TYPE, bean_id).a == "a2"
        assert rb.load(self.BEAN_TYPE, bean_id).b == "b"

        bean = rb.dispense(self.BEAN_TYPE)
        bean.id = bean_id
        bean.a = "a3"
        rb.store(bean)

        assert rb.load(self.BEAN_TYPE, bean_id).a == "a3"
        assert rb.load(self.BEAN_TYPE, bean_id).b is None

    def test_dispense_many(self):
        rb = self.get_red_bean()
        beans = list(rb.dispense_many(self.BEAN_TYPE, count=2))
        assert len(beans) == 2
        assert beans[0].id != beans[1].id

        beans = list(
            rb.dispense_many(
                "alternative_way", data=[{"a": "b"}, {"b": "b", "c": "c"}, {"d": "d"}]
            )
        )
        assert len(beans) == 3
        assert beans[0].id != beans[1].id != beans[2].id
        rb.store_many(beans)
        beans = list(rb.load_many("alternative_way", [b.id for b in beans]))
        assert [dict(b) for b in beans] == [
            {"a": "b", "b": None, "c": None, "d": None, "id": beans[0].id},
            {"a": None, "b": "b", "c": "c", "d": None, "id": beans[1].id},
            {"a": None, "b": None, "c": None, "d": "d", "id": beans[2].id},
        ]

        beans = list(Beans(self.BEAN_TYPE, data=[{"a": "b"}, {"b": "b"}]))
        assert len(beans) == 2
        assert beans[0].id != beans[1].id
        rb.store_many(beans)
        beans = list(rb.load_many(self.BEAN_TYPE, [b.id for b in beans]))
        assert [dict(b) for b in beans] == [
            {"a": "b", "b": None, "id": beans[0].id},
            {"a": None, "b": "b", "id": beans[1].id},
        ]

        with pytest.raises(IncorrectValueError):
            list(rb.dispense_many(self.BEAN_TYPE))

        with pytest.raises(IncorrectValueError):
            list(rb.dispense_many(self.BEAN_TYPE, count=-1))
        with pytest.raises(IncorrectValueError):
            list(rb.dispense_many(self.BEAN_TYPE, count=0))
        with pytest.raises(IncorrectValueError):
            list(rb.dispense_many(self.BEAN_TYPE, count=1.1))
        with pytest.raises(IncorrectValueError):
            list(rb.dispense_many(self.BEAN_TYPE, count=[123]))

        with pytest.raises(IncorrectValueError):
            list(rb.dispense_many(self.BEAN_TYPE, data=123.11))

        with pytest.raises(IncorrectValueError):
            list(rb.dispense_many(self.BEAN_TYPE, count=2, data=[{"a": "b"}]))
