import shutil

import pytest

from redbeanpython import NotExistsError
from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanCreateStructureOnFreeze(RedBeanTestAbstract):
    def test_on_freeze_from_models(self):
        test_data_dir = "tests/resources/migrations/create_structure_on_freeze_test"
        test_namespace = f"freeze_test{self.test_hash()}"

        rb = self.get_red_bean()
        with pytest.raises(NotExistsError):
            _ = self.get_red_bean(frozen=True)

        shutil.copytree(f"{test_data_dir}", f"/tmp/{test_namespace}")
        self.execute_migrations(f"/tmp/{test_namespace}/migrations", rb)
        rb = self.get_red_bean(
            frozen=True, namespace=test_namespace, directory=f"/tmp/{test_namespace}"
        )

        bean = rb.load("abcd", "1234")
        assert "name" in bean
        assert "second_name" not in bean
        assert bean.second_name is None
