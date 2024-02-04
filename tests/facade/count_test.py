from unittest.mock import Mock
from unittest.mock import patch

from tests.facade.abstract import FacadeTestAbstract


class TestFacadeCount(FacadeTestAbstract):
    @patch("redbeanpython.facade.RedBean")
    def test(self, rb_class_mock: Mock):
        rb_mock = rb_class_mock.return_value = Mock()
        rb_mock.count.return_value = 10
        self.initialize()
        assert self.facade.count("bean_type") == 10
        rb_mock.count.assert_called_once_with("bean_type", query=None, params=None)

    @patch("redbeanpython.facade.RedBean")
    def test_with_params(self, rb_class_mock: Mock):
        rb_mock = rb_class_mock.return_value = Mock()
        rb_mock.count.return_value = 10
        self.initialize()
        assert self.facade.count("bean_type", query="x > :x", params={"x": 1}) == 10
        rb_mock.count.assert_called_once_with(
            "bean_type", query="x > :x", params={"x": 1}
        )

    @patch("redbeanpython.facade.RedBean")
    def test_has_to_be_initialized_first(self, _):
        self.assert_is_initialized(lambda: self.facade.count("any_type"))
