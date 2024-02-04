from uuid import uuid4

from tests.abstract import TestAbstract


class BeanTestAbstract(TestAbstract):
    @staticmethod
    def _assert_is_correct_id(bean_id: str):
        assert bean_id is not None
        assert isinstance(bean_id, str)
        assert len(bean_id) == len(str(uuid4()))
