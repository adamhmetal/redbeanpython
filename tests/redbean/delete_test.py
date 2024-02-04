import pytest

from redbeanpython import IncorrectValueError
from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanBase(RedBeanTestAbstract):
    def test_delete(self):
        rb = self.get_red_bean()
        bean = rb.dispense(self.BEAN_TYPE, data={"a": "A"})
        rb.store(bean)
        assert rb.count(self.BEAN_TYPE) == 1

        rb.delete(bean=bean)
        assert rb.count(self.BEAN_TYPE) == 0

        rb.store(bean)
        assert rb.count(self.BEAN_TYPE) == 1

        rb.delete(bean_type=self.BEAN_TYPE, bean_id=bean.id)
        assert rb.count(self.BEAN_TYPE) == 0

        with pytest.raises(IncorrectValueError):
            rb.delete(bean=bean, bean_type=self.BEAN_TYPE, bean_id=bean.id)

        with pytest.raises(IncorrectValueError):
            rb.delete()
