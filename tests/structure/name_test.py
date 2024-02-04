from redbeanpython.structure.db_structure import DbStructure
from tests.structure.abstract import StructureTestAbstract


class TestModelNames(StructureTestAbstract):
    def test_model_name(self):
        assert DbStructure.table_to_model_name("a") == "A"
        assert DbStructure.table_to_model_name("abc") == "Abc"
        assert DbStructure.table_to_model_name("abc_def") == "AbcDef"
        assert DbStructure.table_to_model_name("some_2_name1") == "Some2Name1"
        assert DbStructure.table_to_model_name("_a") == "_A"
        assert DbStructure.table_to_model_name("abc_def_") == "AbcDef_"
        assert DbStructure.table_to_model_name("_abc_def") == "_AbcDef"
