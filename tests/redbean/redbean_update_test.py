from datetime import date

from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanUpdate(RedBeanTestAbstract):
    def test_update(self):
        rb = self.get_red_bean()

        bean = rb.dispense(self.BEAN_TYPE)
        bean.name = "Adam"
        bean.age = 123
        bean.date = date.today()
        rb.store(bean)

        bean = rb.dispense(self.BEAN_TYPE)
        rb.store(bean)

        assert rb.count(self.BEAN_TYPE) == 2
        assert rb.load(self.BEAN_TYPE, bean.id).name is None
        assert rb.load(self.BEAN_TYPE, bean.id).age is None
        assert rb.load(self.BEAN_TYPE, bean.id).date is None

        bean = rb.load(self.BEAN_TYPE, bean.id)
        bean.name = "Adam2"
        bean.date = date.fromisoformat("2020-01-01")
        rb.store(bean)

        assert rb.count(self.BEAN_TYPE) == 2
        assert rb.load(self.BEAN_TYPE, bean.id).name == "Adam2"
        assert rb.load(self.BEAN_TYPE, bean.id).age is None
        assert rb.load(self.BEAN_TYPE, bean.id).date == date.fromisoformat("2020-01-01")
