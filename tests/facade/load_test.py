from unittest.mock import Mock
from unittest.mock import patch

from redbeanpython import Bean
from tests.facade.abstract import FacadeTestAbstract


class TestFacadeStore(FacadeTestAbstract):
    @patch("redbeanpython.facade.RedBean")
    def test(self, rb_class_mock: Mock):
        rb_mock = rb_class_mock.return_value = Mock()
        self.initialize()
        assert self.facade.load("bean_type", "id")
        rb_mock.load.assert_called_once_with("bean_type", "id", throw_on_empty=False)
        assert self.facade.load_many("bean_type", ["id", "id2"])
        rb_mock.load_many.assert_called_once_with(
            "bean_type", ["id", "id2"], throw_on_empty=False
        )

    @patch("redbeanpython.facade.RedBean")
    def test_has_to_be_initialized_first(self, _):
        self.assert_is_initialized(lambda: self.facade.load(Bean("any_type")))
        self.assert_is_initialized(lambda: self.facade.load_many([Bean("any_type")]))
