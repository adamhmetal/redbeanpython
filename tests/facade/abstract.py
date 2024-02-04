from typing import Callable

import pytest

from redbeanpython import NotInitializedError
from redbeanpython import r
from redbeanpython.facade import Facade
from tests.abstract import TestAbstract


class FacadeTestAbstract(TestAbstract):
    def setup(self):
        self.facade: Facade = r

    def initialize(self):
        self.facade.setup("sqlite:////tmp/any.sqlite")

    @staticmethod
    def assert_is_initialized(call: Callable):
        with pytest.raises(NotInitializedError):
            call()
