from unittest.mock import Mock
from unittest.mock import patch

from redbeanpython import Bean
from tests.facade.abstract import FacadeTestAbstract


class TestFacadeStore(FacadeTestAbstract):
    @patch("redbeanpython.facade.RedBean")
    def test(self, rb_class_mock: Mock):
        rb_mock = rb_class_mock.return_value = Mock()
        self.initialize()
        bean = Bean("bean_type")
        bean2 = Bean("bean_type")
        assert self.facade.store(bean)
        rb_mock.store.assert_called_once_with(bean)
        assert self.facade.store_many([bean, bean2])
        rb_mock.store_many.assert_called_once_with([bean, bean2])

    @patch("redbeanpython.facade.RedBean")
    def test_has_to_be_initialized_first(self, _):
        self.assert_is_initialized(lambda: self.facade.store(Bean("any_type")))
        self.assert_is_initialized(lambda: self.facade.store_many([Bean("any_type")]))
