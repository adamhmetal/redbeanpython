from datetime import datetime
from uuid import uuid4

import pytest

from redbeanpython import FrozenError
from redbeanpython import IncorrectNameError
from redbeanpython import IncorrectValueError
from redbeanpython import NotExistsError
from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanBase(RedBeanTestAbstract):
    def test_base_path_of_storing_extending_and_fetching_results(self):
        namespace = f"test_via_env_dir{self.test_hash()}"
        directory = f"/tmp/{namespace}"

        rb = self.get_red_bean(directory=directory, namespace=namespace)
        bean = rb.dispense(self.BEAN_TYPE, data={"a": "A"})
        id_ = bean.id
        assert len(id_) == len(str(uuid4()))
        rb.store(bean)
        bean.b = "B"
        rb.store(bean)
        bean = rb.load(self.BEAN_TYPE, bean.id)
        bean.c = "C"
        rb.store(bean)

        rb = self.get_red_bean(directory=directory, namespace=namespace, frozen=True)

        bean = rb.load(self.BEAN_TYPE, bean.id)
        bean.b = "new_b"
        rb.store(bean)

        bean = rb.load(self.BEAN_TYPE, bean.id)

        assert bean["a"] == "A"
        assert bean["b"] == "new_b"
        assert bean["c"] == "C"
        assert bean["id"] == id_

        assert bean.a == "A"
        assert bean.b == "new_b"
        assert bean.c == "C"
        assert bean.id == id_

        assert rb.count(self.BEAN_TYPE) == 1

        rb.delete(bean=bean)

        with pytest.raises(NotExistsError):
            rb.load(self.BEAN_TYPE, bean.id, throw_on_empty=True)

        assert rb.count(self.BEAN_TYPE) == 0

        rb.delete(bean=bean)

    def test_restricted_keywords_works_properly(self):
        rb = self.get_red_bean()
        bean = rb.dispense("bean_type1")

        bean.id = "id_overriden"
        with pytest.raises(IncorrectValueError):
            bean.id = 1
        with pytest.raises(IncorrectNameError):
            bean.keys = 1

        with pytest.raises(IncorrectValueError):
            bean.datetime_1 = datetime.fromisoformat(f"2001-01-01 00:00:00T+04:00")

        bean.alter = "alter"
        bean.join = "join"
        bean.select = "select"
        bean.public = "public"
        bean.key = "key"
        rb.store(bean)

        bean = rb.load("bean_type1", bean.id)
        assert bean.id == "id_overriden"
        assert bean.alter == "alter"
        assert bean.join == "join"
        assert bean.select == "select"
        assert bean.public == "public"
        assert bean.key == "key"

        assert bean["id"] == "id_overriden"
        assert bean["alter"] == "alter"
        assert bean["join"] == "join"
        assert bean["select"] == "select"
        assert bean["public"] == "public"
        assert bean["key"] == "key"

    def test_cant_change_on_frozen(self):
        namespace = f"test_via_env_dir{self.test_hash()}"
        directory = f"/tmp/{namespace}"

        rb = self.get_red_bean(directory=directory, namespace=namespace)
        bean = rb.dispense(self.BEAN_TYPE, data={"a": "a"})
        rb.store(bean)

        rb = self.get_red_bean(
            directory=directory,
            namespace=namespace,
            frozen=True,
        )
        bean.a = "new_a"
        rb.store(bean)
        with pytest.raises(FrozenError):
            bean["b"] = "b"
            rb.store(bean)
