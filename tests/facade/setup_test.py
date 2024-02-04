from unittest.mock import Mock
from unittest.mock import patch

import pytest

from redbeanpython import NotInitializedError
from redbeanpython.errors import InitializationError
from tests.facade.abstract import FacadeTestAbstract


class TestFacadeSetup(FacadeTestAbstract):
    @patch("redbeanpython.facade.RedBean")
    def test_setup_empty_dsn(self, rb_class_mock: Mock):
        self.facade.setup(None)
        rb_class_mock.assert_called_once_with(
            dsn=None, frozen=False, directory=None, namespace=None
        )

    @patch("redbeanpython.facade.RedBean")
    def test_setup(self, rb_class_mock: Mock):
        with pytest.raises(NotInitializedError):
            self.facade.load("any", "any")
        dsn = "sqlite:///rb.sqlite"
        self.facade.setup(dsn)
        _ = self.facade.load("any", "any")
        rb_class_mock.assert_called_once_with(
            dsn=dsn, frozen=False, directory=None, namespace=None
        )

    @patch("redbeanpython.facade.RedBean")
    def test_setup_frozen(self, rb_class_mock: Mock):
        self.facade.setup(None, frozen=True)
        rb_class_mock.assert_called_once_with(
            dsn=None, frozen=True, directory=None, namespace=None
        )

    @patch("redbeanpython.facade.RedBean")
    def test_setup_other_namespaces(self, rb_class_mock: Mock):
        self.facade.setup(None, directory="dir_x", namespace="namespace_x")
        rb_class_mock.assert_called_once_with(
            dsn=None, frozen=False, directory="dir_x", namespace="namespace_x"
        )

    @patch("redbeanpython.facade.RedBean")
    def test_setup_many_times_with_same_dsn_should_pass(self, rb_class_mock: Mock):
        dsn = "sqlite:///rb.sqlite"
        self.facade.setup(dsn)
        self.facade.setup(dsn)
        self.facade.setup(dsn=dsn)
        self.facade.setup(dsn=dsn)
        rb_class_mock.assert_called_once_with(
            dsn=dsn, frozen=False, directory=None, namespace=None
        )

    @patch("redbeanpython.facade.RedBean")
    def test_setup_with_different_settings(self, _):
        dsn = "sqlite:///rb.sqlite"
        self.facade.setup(dsn)
        with pytest.raises(InitializationError):
            self.facade.setup("sqlite:///other_data_base.sqlite")
        with pytest.raises(InitializationError):
            self.facade.setup(dsn, frozen=True)
        with pytest.raises(InitializationError):
            self.facade.setup(dsn, directory="other")
        with pytest.raises(InitializationError):
            self.facade.setup(dsn, namespace="other")
        with pytest.raises(InitializationError):
            self.facade.setup(False, namespace="other")
        with pytest.raises(InitializationError):
            self.facade.setup(namespace="other")
