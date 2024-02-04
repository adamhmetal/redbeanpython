from unittest.mock import Mock
from unittest.mock import patch

from redbeanpython import Bean
from tests.facade.abstract import FacadeTestAbstract


class TestFacadeFind(FacadeTestAbstract):
    @patch("redbeanpython.facade.RedBean")
    def test(self, rb_class_mock: Mock):
        bean = Bean("bean_type")
        rb_mock = rb_class_mock.return_value = Mock()
        rb_mock.find.return_value = bean
        self.initialize()
        assert self.facade.find("bean_type") == bean
        rb_mock.find.assert_called_once_with(
            "bean_type", query=None, params=None, order=None, limit=None, offset=None
        )

    @patch("redbeanpython.facade.RedBean")
    def test_with_params(self, rb_class_mock: Mock):
        bean = Bean("bean_type")
        rb_mock = rb_class_mock.return_value = Mock()
        rb_mock.find.return_value = bean
        self.initialize()
        assert (
            self.facade.find(
                "bean_type",
                query="x > :x",
                params={"x": 1},
                order="z",
                limit=1,
                offset=2,
            )
            == bean
        )
        rb_mock.find.assert_called_once_with(
            "bean_type", query="x > :x", params={"x": 1}, order="z", limit=1, offset=2
        )

    @patch("redbeanpython.facade.RedBean")
    def test_has_to_be_initialized_first(self, _):
        self.assert_is_initialized(lambda: self.facade.find("any_type"))
