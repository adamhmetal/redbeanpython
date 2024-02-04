import warnings
from importlib import import_module

from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanViaModel(RedBeanTestAbstract):
    def test_operating_via_sqlalchemy_model_directly(self):
        rb = self.get_red_bean()
        bean = rb.dispense("test")
        bean.name = "name"
        bean.value = "value"
        rb.store(bean)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            module = import_module(f"{rb.config.namespace}.models.test")
        test_model_class = getattr(module, "Test")
        test_model = test_model_class()
        test_model.id = "1234"
        test_model.name = "name2"
        test_model.value = "value2"
        with rb.session_maker() as session:
            session.add(test_model)
            session.commit()

        bean = rb.load("test", "1234")
        assert bean.id == "1234"
        assert bean.name == "name2"
        assert bean.value == "value2"

        with rb.session_maker() as session:
            e = session.get(test_model_class, "1234")
            assert e.id == "1234"
            assert e.name == "name2"
            assert e.value == "value2"
