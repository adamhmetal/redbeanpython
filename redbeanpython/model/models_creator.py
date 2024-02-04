import os
import warnings
from importlib import import_module
from importlib import reload

from mako.template import Template

from redbeanpython.const import TEMPLATES_DIR
from redbeanpython.structure.table import TableDefinition


class ModelsCreator:
    def __init__(self, directory: str, namespace: str):
        self._directory = directory
        self._namespace = namespace

    def create_model(self, model_name: str, table: TableDefinition) -> None:
        self._create_model_file(model_name, table)
        self._load_model(model_name, table.name)

    def _create_model_file(self, model_name: str, table: TableDefinition) -> None:
        alchemy_types = [table.alchemy_type for table in table.columns.values()]
        unique_alchemy_types = list(dict.fromkeys(alchemy_types))
        model_content = Template(filename=os.path.join(TEMPLATES_DIR, "model.py.mako")).render(
            sqlalchemy_types=unique_alchemy_types,
            table_name=table.name,
            model_name=model_name,
            columns=table.columns,
        )
        model_file = f"{os.path.join(self._directory, 'models', table.name)}.py"
        if not os.path.exists(dirname := os.path.dirname(model_file)):
            os.makedirs(dirname)
        with open(model_file, "w") as f:
            f.write(model_content)

    def _load_model(self, model_name: str, table_name: str) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            module = import_module(f"{self._namespace}.models.{table_name}")
            module = reload(module)

        _ = getattr(module, model_name)
