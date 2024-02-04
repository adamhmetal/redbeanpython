from datetime import date, datetime
from decimal import Decimal
from typing import Callable

import pytest

from redbeanpython import FrozenError, RedBean
from tests.abstract import TestAbstract


class RedBeanTestAbstract(TestAbstract):
    @staticmethod
    def assert_bean_exists(rb: RedBean, bean_type: str, bean_id: str):
        assert rb.exists(bean_type, bean_id=bean_id)

    @staticmethod
    def assert_bean_not_exists(rb: RedBean, bean_type: str, bean_id: str):
        assert not rb.exists(
            bean_type, bean_id=bean_id + "s"
        ), f"Bean {bean_id} should not exist"

    @staticmethod
    def assert_raise_in_frozen_mode(call: Callable):
        with pytest.raises(FrozenError):
            call()

    @staticmethod
    def generate_bean_content(test_hash: int = 1):
        return {
            f"bool_{test_hash}": True,
            f"int_{test_hash}": test_hash,
            f"string_{test_hash}": f"any_{test_hash}",
            f"float_{test_hash}": test_hash + 0.1,
            f"decimal_{test_hash}": Decimal(f"{test_hash}.5"),
            f"datetime_{test_hash}": datetime.fromisoformat(
                f"{2000+test_hash}-01-01 00:00:00"
            ),
            f"date_{test_hash}": date.fromisoformat(f"{2000+test_hash}-01-01"),
        }
