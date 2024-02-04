import os
import sys
from uuid import uuid4

import sqlalchemy
from alembic import command
from alembic.config import Config

from redbeanpython.redbean import RedBean


# noinspection PyAttributeOutsideInit
class TestAbstract:
    BEAN_TYPE = "test"

    # noinspection PyMethodMayBeStatic
    def setup(self):
        self.clear_database()

    @staticmethod
    def execute_migrations(migrations_dir: str, rb: RedBean):
        alembic_cfg = Config()
        alembic_cfg.set_main_option("script_location", migrations_dir)
        alembic_cfg.set_main_option("sqlalchemy.url", rb.config.dsn)
        # list all file sin migrations dir
        command.upgrade(alembic_cfg, "head")

    @staticmethod
    def clear_database():
        if "/tmp/" not in sys.path:
            sys.path.append("/tmp/")
        dsn = os.environ.get("DB_DSN")
        match os.environ.get("DB_TYPE"):
            case "sqlite":
                db_path = dsn.replace("sqlite:///", "")
                if os.path.exists(db_path):
                    os.remove(db_path)
            case "postgres":
                e = sqlalchemy.create_engine(dsn)
                connection = e.connect()
                connection.execute(
                    sqlalchemy.text("DROP SCHEMA IF EXISTS public CASCADE")
                )
                connection.execute(sqlalchemy.text("CREATE SCHEMA public"))
                connection.commit()
            case "mysql":
                e = sqlalchemy.create_engine(dsn)
                db_name = dsn.split("/")[-1]
                connection = e.connect()
                connection.execute(
                    sqlalchemy.text(f"DROP DATABASE IF EXISTS {db_name}")
                )
                connection.execute(sqlalchemy.text(f"CREATE DATABASE {db_name}"))
                connection.commit()
            case _:
                raise ValueError(f"Unknown DB_TYPE: {os.environ.get('DB_TYPE')}")

    @staticmethod
    def test_hash():
        return str(uuid4()).replace("-", "")

    def get_red_bean(
        self,
        *,
        namespace: str = None,
        directory: str = None,
        frozen: bool = None,
        dsn: str = None,
    ) -> RedBean:
        namespace = namespace or f"redbean{self.test_hash()}"
        directory = directory or f"/tmp/{namespace}"
        frozen = frozen or False

        return RedBean(
            dsn=dsn or os.environ.get("DB_DSN"),
            frozen=frozen,
            directory=directory,
            namespace=namespace,
        )
