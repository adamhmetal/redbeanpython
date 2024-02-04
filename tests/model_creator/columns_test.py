from datetime import date
from datetime import datetime
from decimal import Decimal

from redbeanpython.model.models_creator import ModelsCreator
from redbeanpython.structure.table import TableDefinition
from tests.model_creator.abstract import ModelCreatorTestAbstract


class TestColumns(ModelCreatorTestAbstract):
    def test_model_created_correctly(self):
        namespace = 'redbean' + self.test_hash()
        directory = f'/tmp/{namespace}'
        rb = self.get_red_bean()
        mc = ModelsCreator(directory=directory, namespace=namespace)

        bean = rb.dispense('some_name')
        bean['value'] = 1

        table = TableDefinition.extend(None, bean)

        mc.create_model(model_name='SomeName', table=table)

        self.assert_model_equals(expected_file='single_int_model.txt', got_file=directory + '/models/some_name.py')

    def test_model_created_correctly_with_all_types(self):
        namespace = 'redbean' + self.test_hash()
        directory = f'/tmp/{namespace}'
        rb = self.get_red_bean()
        mc = ModelsCreator(directory=directory, namespace=namespace)

        bean = rb.dispense('some_name')
        bean['int'] = 1
        bean['float'] = 1.1
        bean['decimal'] = Decimal('1.1')
        bean['string'] = 'string'
        bean['text'] = 'x' * 1000
        bean['bool'] = True
        bean['bytes'] = b"123"
        bean['datetime'] = datetime.fromisoformat('2021-01-01 00:00:00')
        bean['date'] = date.fromisoformat('2021-01-01')

        table = TableDefinition.extend(None, bean)

        mc.create_model(model_name="SomeName", table=table)

        self.assert_model_equals(expected_file='all_types_model.txt', got_file=directory + '/models/some_name.py')
