from unittest.mock import Mock
from unittest.mock import patch

from tests.facade.abstract import FacadeTestAbstract


class TestFacadeNuke(FacadeTestAbstract):
    @patch("redbeanpython.facade.RedBean")
    def test(self, rb_class_mock: Mock):
        rb_mock = rb_class_mock.return_value = Mock()
        rb_mock.exists.return_value = True
        self.initialize()
        assert self.facade.exists("bean_type", bean_id="bean_id") is True
        rb_mock.exists.assert_called_once_with("bean_type", bean_id="bean_id")

        rb_mock.exists.return_value = False
        assert self.facade.exists("bean_type", bean_id="bean_id") is False

    @patch("redbeanpython.facade.RedBean")
    def test_has_to_be_initialized_first(self, _):
        self.assert_is_initialized(
            lambda: self.facade.exists("bean_type", bean_id="bean_id")
        )
