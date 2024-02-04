from unittest.mock import Mock
from unittest.mock import patch

from tests.facade.abstract import FacadeTestAbstract


class TestFacadeDispense(FacadeTestAbstract):
    @patch("redbeanpython.facade.RedBean")
    def test(self, rb_class_mock: Mock):
        rb_mock = rb_class_mock.return_value = Mock()
        rb_mock.dispense.return_value = "dispense"
        rb_mock.dispense_many.return_value = "dispense_many"
        self.initialize()
        assert self.facade.dispense("bean_type") == "dispense"
        rb_mock.dispense.assert_called_once_with("bean_type")
        assert self.facade.dispense_many("bean_type", count=2) == "dispense_many"
        rb_mock.dispense_many.assert_called_once_with("bean_type", count=2, data=None)
        assert (
            self.facade.dispense_many("bean_type", data=[{"x": 1}]) == "dispense_many"
        )
        rb_mock.dispense_many.assert_called_with(
            "bean_type", data=[{"x": 1}], count=None
        )

    @patch("redbeanpython.facade.RedBean")
    def test_has_to_be_initialized_first(self, _):
        self.assert_is_initialized(lambda: self.facade.dispense("any_type"))
        self.assert_is_initialized(lambda: self.facade.dispense_many("any_type"))
