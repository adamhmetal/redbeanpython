import pytest

from redbeanpython.errors import IncorrectNameError
from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanValidation(RedBeanTestAbstract):
    def test_snake_case_default(self):
        rb = self.get_red_bean()
        for name in ["case", "snake_case", "snake_case_1", "class"]:
            bean = rb.dispense(name)
            assert bean.bean_type == name
            bean[name] = name
            assert bean[name] == name

        with pytest.raises(IncorrectNameError):
            rb.dispense(object())
        bean = rb.dispense("x")
        with pytest.raises(IncorrectNameError):
            bean[object()] = "x"

        for name in [
            "",
            "_snake_case",
            "CamelC",
            "space case",
            "1_case",
            "case-1",
            "case#x",
            "camelCase",
            1,
            {},
            None,
        ]:
            with pytest.raises(IncorrectNameError):
                rb.dispense(name)
            bean = rb.dispense("x")
            with pytest.raises(IncorrectNameError):
                bean[name] = "x"
