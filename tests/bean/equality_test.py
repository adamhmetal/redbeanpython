from redbeanpython import Bean

from tests.bean.abstract import BeanTestAbstract


class TestBeanValidation(BeanTestAbstract):
    def test_equality(self):
        example_data = {"id": "1"}
        example_data_2 = {"id": "1", "b": "b", "c": "c"}

        assert Bean("any") != "any"
        assert Bean("any") != Bean("any")
        assert Bean("any", example_data) == Bean("any", example_data)

        bean = self.get_red_bean().dispense("any", data=example_data)

        assert Bean("any", example_data) == bean
        assert Bean("any", example_data_2) != bean

        bean["b"] = "b"
        bean.c = "c"

        assert Bean("any", example_data_2) == bean
        assert dict(Bean("any", example_data_2)) == example_data_2

        assert Bean("any", example_data_2) != dict(bean)
        assert Bean("any", example_data_2) != example_data_2
        assert Bean("any", example_data_2) != Bean("other", example_data_2)
