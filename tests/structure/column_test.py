from redbeanpython.structure.type import TypeFactory
from tests.structure.abstract import StructureTestAbstract


class TestColumnDefinition(StructureTestAbstract):
    def test_equality(self):
        column = TypeFactory.from_value("x", "a")

        assert column == TypeFactory.from_value("x", "zzzz")
        assert column == TypeFactory.from_sql("x", "Text()")

        assert column != "other_type"
        assert column != TypeFactory.from_value("id", "a")
        assert column != TypeFactory.from_value("x", 1.1)
        assert column != TypeFactory.from_value("x", True)
