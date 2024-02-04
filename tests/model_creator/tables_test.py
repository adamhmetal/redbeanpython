from redbeanpython.model.models_creator import ModelsCreator
from redbeanpython.structure.table import TableDefinition
from tests.model_creator.abstract import ModelCreatorTestAbstract


class TestTables(ModelCreatorTestAbstract):
    def test_model_created_correctly(self):
        rb = self.get_red_bean()
        bean = rb.dispense("some_2_name1")
        bean["value"] = 1

        namespace = "redbean" + self.test_hash()
        directory = f"/tmp/{namespace}"
        mc = ModelsCreator(directory=directory, namespace=namespace)

        table = TableDefinition.extend(None, bean)
        mc.create_model(model_name="Some2Name1", table=table)

        self.assert_model_equals(
            expected_file="name_model.txt",
            got_file=directory + "/models/some_2_name1.py",
        )

    def test_equality(self):
        rb = self.get_red_bean()

        bean = rb.dispense("any")
        other_bean = rb.dispense("other")

        assert TableDefinition.extend(None, bean) == TableDefinition.extend(None, bean)

        assert TableDefinition.extend(None, bean) != TableDefinition.extend(
            None, rb.dispense("other")
        )
        assert TableDefinition.extend(None, bean) != TableDefinition.extend(
            None, other_bean
        )
