from unittest.mock import Mock
from unittest.mock import patch

from tests.facade.abstract import FacadeTestAbstract


class TestFacadeEngine(FacadeTestAbstract):
    @patch("redbeanpython.facade.RedBean")
    def test_engine(self, rb_class_mock: Mock):
        rb_mock = rb_class_mock.return_value = Mock()
        rb_mock.engine = "mocked"
        self.initialize()
        assert self.facade.engine == "mocked"

    @patch("redbeanpython.facade.RedBean")
    def test_engine_has_to_be_initialized_first(self, _):
        self.assert_is_initialized(lambda: self.facade.engine)

    @patch("redbeanpython.facade.RedBean")
    def test_session_maker(self, rb_class_mock: Mock):
        rb_mock = rb_class_mock.return_value = Mock()
        rb_mock.session_maker = "mocked"
        self.initialize()
        assert self.facade.session_maker == "mocked"

    @patch("redbeanpython.facade.RedBean")
    def test_session_maker_has_to_be_initialized_first(self, _):
        self.assert_is_initialized(lambda: self.facade.session_maker)

