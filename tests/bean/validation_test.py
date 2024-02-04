import pytest

from redbeanpython import Bean, IncorrectNameError, IncorrectValueError

from tests.bean.abstract import BeanTestAbstract


class TestBeanValidation(BeanTestAbstract):
    def test_validation(self):
        with pytest.raises(IncorrectNameError):
            Bean("Wrong")
        with pytest.raises(IncorrectNameError):
            Bean("_wrong")

        bean = Bean(self.BEAN_TYPE)

        with pytest.raises(IncorrectNameError):
            bean.Name = "a"
        with pytest.raises(IncorrectNameError):
            bean._name = "a"

        bean.name = "any_name"
        with pytest.raises(IncorrectValueError):
            bean.name = {}
