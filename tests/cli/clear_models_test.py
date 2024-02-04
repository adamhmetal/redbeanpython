import os.path
from unittest.mock import Mock
from unittest.mock import patch

from tests.cli.abstract import RedBeanCliTestAbstract


class TestCliClearModels(RedBeanCliTestAbstract):
    @patch("redbeanpython.cli.cli.ArgumentParser")
    def test_cli_call(self, parser_mock: Mock):
        parser_mock.return_value = parser_instance = Mock()
        parser_instance.parse_args.return_value = type(
            "obj", (object,), {"command": "not_existing"}
        )
        self.execute(["not_existing"])

    def test_clear_models(self):
        sqlite_test_file = f"/tmp/clear_models_{self.test_hash()}.sqlite"
        namespace = f"nuke_{self.test_hash()}"
        directory = f"/tmp/{namespace}"
        dsn = f"sqlite:///{sqlite_test_file}"
        self._create_test_entry(dsn, directory, namespace)
        assert os.path.exists(sqlite_test_file)

        envs = {
            "REDBEAN_DB_DSN": dsn,
            "REDBEAN_NAMESPACE": namespace,
            "REDBEAN_DIRECTORY": directory,
        }

        with patch.dict("os.environ", envs):
            self.execute(["clear_models"])

        assert not os.path.exists(f"{directory}/models/a.py")
        assert not os.path.exists(f"{directory}/migrations/versions/001_.py")

        rb = self.get_red_bean(dsn=dsn)
        assert rb.count(self.BEAN_TYPE) == 1

    def test_clear_models_with_params(self):
        sqlite_test_file = f"/tmp/clear_models_{self.test_hash()}.sqlite"
        namespace = f"nuke_{self.test_hash()}"
        directory = f"/tmp/{namespace}"
        dsn = f"sqlite:///{sqlite_test_file}"
        self._create_test_entry(dsn, directory, namespace)
        assert os.path.exists(sqlite_test_file)

        self.execute(["clear_models", "--directory", directory])

        assert not os.path.exists(f"{directory}/models/a.py")
        assert not os.path.exists(f"{directory}/migrations/versions/001_.py")

        rb = self.get_red_bean(dsn=dsn)
        assert rb.count(self.BEAN_TYPE) == 1
