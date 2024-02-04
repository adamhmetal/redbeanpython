from unittest.mock import Mock
from unittest.mock import patch

from redbeanpython import Bean
from tests.facade.abstract import FacadeTestAbstract


class TestFacadeDelete(FacadeTestAbstract):
    @patch("redbeanpython.facade.RedBean")
    def test(self, rb_class_mock: Mock):
        rb_mock = rb_class_mock.return_value = Mock()
        self.initialize()
        bean = Bean("any_type")
        self.facade.delete(bean=bean)
        rb_mock.delete.assert_called_once_with(bean=bean, bean_type=None, bean_id=None)
        self.facade.delete(bean_type="any_type", bean_id="any_id")
        rb_mock.delete.assert_called_with(
            bean=None, bean_type="any_type", bean_id="any_id"
        )

    @patch("redbeanpython.facade.RedBean")
    def test_has_to_be_initialized_first(self, _):
        self.assert_is_initialized(lambda: self.facade.delete(bean=Bean("any_type")))
