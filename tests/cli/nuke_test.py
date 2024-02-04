import os.path
from unittest.mock import patch

import pytest

from redbeanpython.cli.cli import CommandError
from tests.cli.abstract import RedBeanCliTestAbstract


class TestCliNuke(RedBeanCliTestAbstract):
    def test_nuke(self):
        sqlite_test_file = f"/tmp/nuke_{self.test_hash()}.sqlite"
        namespace = f"nuke_{self.test_hash()}"
        directory = f"/tmp/{namespace}"
        dsn = f"sqlite:///{sqlite_test_file}"
        self._create_test_entry(dsn, directory, namespace)
        assert os.path.exists(sqlite_test_file)

        rb = self.get_red_bean(dsn=dsn)
        assert rb.count(self.BEAN_TYPE) == 1

        envs = {
            "REDBEAN_DB_DSN": dsn,
            "REDBEAN_NAMESPACE": namespace,
            "REDBEAN_DIRECTORY": directory,
        }

        with patch.dict("os.environ", envs):
            self.execute(["nuke"])

        assert not os.path.exists(f"{directory}/models/test.py")
        assert not os.path.exists(f"{directory}/migrations/env.py")

        rb = self.get_red_bean(dsn=dsn)
        assert rb.count(self.BEAN_TYPE) == 0

    def test_nuke_against_remote_database(self):
        envs = {
            "REDBEAN_DB_DSN": "postgresql+psycopg://user:pass@localhost/dbname",
            "REDBEAN_NAMESPACE": "test",
            "REDBEAN_DIRECTORY": "/tmp/test",
        }

        with patch.dict("os.environ", envs):
            self.execute(["nuke"])

        envs["REDBEAN_DB_DSN"] = "postgresql+psycopg://user:pass@example.com/dbname"
        with patch.dict("os.environ", envs):
            with pytest.raises(CommandError):
                self.execute(["nuke"])

    def test_nuke_against_not_existing(self):
        sqlite_test_file = f"/tmp/nuke_{self.test_hash()}.sqlite"
        namespace = f"nuke_{self.test_hash()}"
        directory = f"/tmp/{namespace}"
        dsn = f"sqlite:///{sqlite_test_file}"
        self._create_test_entry(dsn, directory, namespace)
        assert os.path.exists(sqlite_test_file)

        rb = self.get_red_bean(dsn=dsn)
        assert rb.count(self.BEAN_TYPE) == 1

        envs = {
            "REDBEAN_DB_DSN": dsn,
            "REDBEAN_NAMESPACE": namespace,
            "REDBEAN_DIRECTORY": "other_models",
        }

        with patch.dict("os.environ", envs):
            self.execute(["nuke"])

        assert os.path.exists(f"{directory}/models/test.py")
        assert os.path.exists(f"{directory}/migrations/env.py")

        rb = self.get_red_bean(dsn=dsn)
        assert rb.count(self.BEAN_TYPE) == 1

    def test_nuke_with_params(self):
        sqlite_test_file = f"/tmp/nuke_{self.test_hash()}.sqlite"
        namespace = f"nuke_{self.test_hash()}"
        directory = f"/tmp/{namespace}"
        dsn = f"sqlite:///{sqlite_test_file}"
        self._create_test_entry(dsn, directory, namespace)
        assert os.path.exists(sqlite_test_file)

        self.execute(
            [
                "nuke",
                "--dsn",
                dsn,
                "--namespace",
                namespace,
                "--directory",
                directory,
            ]
        )

        assert not os.path.exists(f"{directory}/models/a.py")
        assert not os.path.exists(f"{directory}/migrations/versions/001_.py")

        rb = self.get_red_bean(dsn=dsn)
        assert rb.count(self.BEAN_TYPE) == 0
