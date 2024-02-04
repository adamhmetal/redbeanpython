import logging
import os
import shutil
import sys
import tempfile
import warnings
from argparse import ArgumentParser
from importlib import import_module
from importlib import reload
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


class CommandError(Exception):
    ...


class NukeCommand:
    def run(self, dsn: str, directory: str, namespace: str) -> None:
        dsn = dsn or f"sqlite:///{tempfile.gettempdir()}/redbean.sqlite"
        self._validate_dsn(dsn)
        self.nuke(dsn, os.path.join(os.getcwd(), directory), namespace)

    @staticmethod
    def _validate_dsn(dsn: str) -> None:
        if dsn.startswith("sqlite:"):
            return
        db_address = dsn.split("@")[1]
        if "." in db_address:
            raise CommandError("Nuke can not be fired against remote databases.")

    @staticmethod
    def nuke(dsn: str, directory: str, namespace: str) -> None:
        engine = create_engine(dsn)

        if not os.path.exists(os.path.join(directory, "models")):
            logging.info("No models found. Nothing to nuke.")
            return

        for file_name in os.listdir(os.path.join(directory, "models")):
            sys.path.insert(0, os.path.dirname(os.path.abspath(directory)))
            if not file_name.startswith("_"):
                table_name = file_name.replace(".py", "")
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    module = import_module(f"{namespace}.models.{table_name}")
                    reload(module)

        meta = declarative_base().metadata
        meta.reflect(bind=engine)
        meta.drop_all(bind=engine)

        ClearModelsCommand().clear(directory)


class ClearModelsCommand:
    def run(self, directory: str) -> None:
        self.clear(directory)

    @staticmethod
    def clear(directory: str) -> None:
        shutil.rmtree(os.path.join(directory, "models"))
        shutil.rmtree(os.path.join(directory, "migrations"))


class CommandLine:
    def __init__(self) -> None:
        self._create_parser()

    def _create_parser(self) -> None:
        parser = ArgumentParser(prog="redbean")
        parser.add_argument(
            "command",
            type=str,
            choices=["nuke", "clear_models"],
            help="Command to run",
        )

        parser.add_argument(
            "--dsn",
            type=str,
            default=os.environ.get("REDBEAN_DB_DSN", None),
            help="DSN to connect to the database",
        )
        parser.add_argument(
            "--directory",
            type=str,
            default=os.environ.get("REDBEAN_DIRECTORY", "redbean"),
            help="Directory where models are stored",
        )
        parser.add_argument(
            "--namespace",
            type=str,
            default=os.environ.get("REDBEAN_NAMESPACE", "redbean"),
            help="Namespace for models",
        )

        self.parser = parser

    def main(self, argv: list[str] = None) -> None:
        options = self.parser.parse_args(argv)
        match options.command:
            case "nuke":
                return NukeCommand().run(options.dsn, options.directory, options.namespace)
            case "clear_models":
                return ClearModelsCommand().run(options.directory)
            case _:
                print("Command not found")


def main(argv: list[str] | None = None, **_: Any) -> None:
    CommandLine().main(argv=argv)
