import os
import shutil
import warnings
from importlib import import_module
from importlib import reload
from time import time
from typing import Type

from alembic.config import command
from alembic.config import Config as AlembicConfig
from mako.template import Template
from sqlalchemy import Engine
from sqlalchemy.orm import declarative_base

from redbeanpython.bean.bean import Bean
from redbeanpython.const import TEMPLATES_DIR
from redbeanpython.const import TYPE
from redbeanpython.model.model import Model
from redbeanpython.model.models_creator import ModelsCreator
from redbeanpython.redbean import Config
from redbeanpython.structure.column_type import ColumnType
from redbeanpython.structure.table import TableDefinition
from redbeanpython.structure.type import TypeFactory


class DbStructure:
    def __init__(self, engine: Engine, config: Config):
        self.tables: dict[str, TableDefinition] = {}
        self._models_creator = ModelsCreator(config.directory, config.namespace)
        self._engine: Engine = engine
        self._config: Config = config
        self._init()

    def _init(self) -> None:
        self._load_from_database()
        self._load_from_models()

        if not self._config.frozen:
            self._create_models_from_database()

    def get_model_class(self, bean_type: str) -> Model:
        return self._sql_alchemy_model_class(bean_type)

    def have_table(self, bean_type: str) -> bool:
        return bean_type in self.tables

    def get_model(self, bean: Bean) -> Model:
        model_class = self.get_model_class(bean.bean_type)
        return model_class(**dict(bean))

    def get_default_properties(self, bean_type: str) -> dict[str, TYPE]:
        if table_definition := self.tables.get(bean_type):
            return table_definition.get_properties_dict()
        return {}

    def is_table_up_to_date(self, bean: Bean) -> bool:
        current_definition = self.tables.get(bean.bean_type)
        new_definition = TableDefinition.extend(current_definition, bean)
        return new_definition == current_definition

    def update_structure(self, bean: Bean) -> None:
        new_definition = TableDefinition.extend(self.tables.get(bean.bean_type), bean)
        self.tables[bean.bean_type] = new_definition
        self._models_creator.create_model(
            model_name=self.table_to_model_name(bean.bean_type),
            table=new_definition,
        )
        self._create_migrations()

    @staticmethod
    def table_to_model_name(table_name: str) -> str:
        words = table_name.split("_")
        pascal = "".join(word.title() for word in words)
        if table_name.startswith("_"):
            pascal = f"_{pascal}"
        if table_name.endswith("_"):
            pascal = f"{pascal}_"
        return pascal

    def _load_from_database(self) -> None:
        tables: dict[str, TableDefinition] = {}
        meta = declarative_base().metadata
        meta.reflect(bind=self._engine)
        for table in meta.tables.values():
            if table.name == "alembic_version":
                continue
            columns: dict[str, ColumnType] = {}
            for sql_column in table.columns:
                columns[sql_column.name] = TypeFactory.from_sql(
                    column_name=sql_column.name, column_type=str(sql_column.type)
                )
            tables[table.name] = TableDefinition(table.name, columns)

        self.tables = tables

    def _load_from_models(self) -> None:
        if not os.path.exists(self._config.models_directory):
            return

        for file_name in os.listdir(self._config.models_directory):
            if not file_name.startswith("_"):
                table_name = file_name.replace(".py", "")

                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    module = import_module(f"{self._config.namespace}.models.{table_name}")
                    reload(module)

                model_class = getattr(module, self.table_to_model_name(table_name))
                self.tables[table_name] = TableDefinition.from_model_class(table_name, model_class)

    def _create_models(self) -> None:
        for table_name, table in self.tables.items():
            self._models_creator.create_model(
                model_name=self.table_to_model_name(table_name),
                table=table,
            )

    def _sql_alchemy_model_class(self, bean_type: str) -> Type[Model]:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            module = import_module(f"{self._config.namespace}.models.{bean_type}")
        return getattr(module, self.table_to_model_name(bean_type))

    def _create_models_from_database(self) -> None:
        self._init_directory()
        self._create_models()

    def _init_directory(self) -> None:
        migrations_directory = self._config.migrations_directory
        os.makedirs(os.path.join(migrations_directory, "versions"), exist_ok=True)

        src_file = os.path.join(
            TEMPLATES_DIR,
            "env.sqlite.py.template" if self._config.dsn.startswith("sqlite:") else "env.py.template",
        )
        shutil.copy(src_file, os.path.join(migrations_directory, "env.py"))
        shutil.copy(
            os.path.join(TEMPLATES_DIR, "script.py.mako.template"),
            os.path.join(migrations_directory, "script.py.mako"),
        )
        content = Template(filename=os.path.join(TEMPLATES_DIR, "alembic.ini.mako")).render(
            migrations_dir=migrations_directory,
        )
        with open(os.path.join(migrations_directory, "alembic.ini"), "w") as f:
            f.write(content)

    def _create_migrations(self) -> None:
        alembic_cfg = AlembicConfig()

        alembic_cfg.set_main_option("script_location", self._config.migrations_directory)
        alembic_cfg.set_main_option("sqlalchemy.url", self._config.dsn)
        alembic_cfg.set_main_option("DB_DSN.url", self._config.dsn)
        section = alembic_cfg.config_ini_section
        alembic_cfg.set_section_option(section, "DB_DSN", self._config.dsn)
        rev_id = str(round(time() * 1_000_000))
        command.revision(alembic_cfg, rev_id=rev_id, autogenerate=True)
        command.upgrade(alembic_cfg, "head")

        self._load_from_database()
