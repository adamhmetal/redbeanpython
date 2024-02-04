import pytest

from redbeanpython import Bean
from redbeanpython import Id
from redbeanpython import IncorrectNameError
from redbeanpython import IncorrectValueError
from tests.bean.abstract import BeanTestAbstract


class TestBeanOperations(BeanTestAbstract):
    def test_deletion(self):
        bean = Bean(self.BEAN_TYPE)

        del bean["not_existing"]
        del bean.not_existing2

        bean["a"] = "a"
        assert bean.a == "a"
        del bean.a
        assert bean.a is None

        assert "a" not in dict(bean)

        with pytest.raises(IncorrectNameError):
            del bean.Name
        with pytest.raises(IncorrectNameError):
            del bean["_name"]

    def test_id(self):
        bean = Bean(self.BEAN_TYPE)

        self._assert_is_correct_id(bean.id)

        bean["id"] = "123"
        assert bean.id == "123"
        assert bean["id"] == "123"

        bean["id"] = Id("1234")
        assert bean.id == "1234"
        bean["id"] = Id("12345")
        assert bean.id == "12345"
        bean["id"] = Id("123456")
        assert bean.id == "123456"

        with pytest.raises(IncorrectValueError):
            bean.id = 1.1
        with pytest.raises(IncorrectValueError):
            bean.id = 1
        with pytest.raises(IncorrectValueError):
            bean["id"] = 1.1
        with pytest.raises(IncorrectValueError):
            bean["id"] = 1

        with pytest.raises(IncorrectValueError):
            del bean.id
        with pytest.raises(IncorrectValueError):
            del bean["id"]

        with pytest.raises(IncorrectValueError):
            bean["id"] = None
        with pytest.raises(IncorrectValueError):
            bean.id = None

        assert bean.id == "123456"

    def test_repr(self):
        bean = Bean("any", {"id": "1", "b": "b"})

        expected = "Bean(bean_type='any', data={'id': '1', 'b': 'b'})"
        assert repr(bean) == expected
        assert str(bean) == expected

    def test_dict(self):
        bean = Bean("any", {"id": "1", "b": "b"})

        assert dict(bean) == {"id": "1", "b": "b"}

    def test_iter(self):
        rb = self.get_red_bean()

        bean = rb.dispense(self.BEAN_TYPE, data={"a": "A"})
        assert set(list(bean)) == {"id", "a"}
        rb.store(bean)

        bean = rb.dispense(self.BEAN_TYPE)
        bean.b = "B"
        rb.store(bean)

        bean = rb.load(self.BEAN_TYPE, bean.id)
        bean.c = "C"

        assert set(list(bean)) == {"id", "a", "b", "c"}

        self._assert_is_correct_id(bean.id)
        assert bean["a"] is None
        assert bean["b"] == "B"
        assert bean["c"] == "C"
