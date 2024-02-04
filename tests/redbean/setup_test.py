import os
from unittest.mock import patch

import pytest
import sqlalchemy

from redbeanpython import RedBean
from redbeanpython.errors import ConfigurationError
from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanSetup(RedBeanTestAbstract):
    def test_setup_via_env(self):
        for frozen in ["true", "1", "yes", "invalid"]:
            directory = f"/tmp/test_via_env_dir{self.test_hash()}"
            test_namespace = "test_via_env_namespace"
            test_dsn = "sqlite:////tmp/test_via_env.db"

            test_envs = {
                "REDBEAN_DB_DSN": test_dsn,
                "REDBEAN_DB_FROZEN": frozen,
                "REDBEAN_NAMESPACE": test_namespace,
                "REDBEAN_DIRECTORY": directory,
            }

            os.makedirs(f"{directory}/models", exist_ok=True)
            os.makedirs(f"{directory}/migrations/versions", exist_ok=True)

            with patch.dict("os.environ", test_envs):
                rb = RedBean()
            assert rb.config.dsn == test_dsn
            assert rb.config.directory == directory
            assert rb.config.namespace == test_namespace
            assert rb.config.frozen is True

    def test_setup_fluid_via_env(self):
        for frozen in ["0", "false", "no"]:
            test_envs = {
                "REDBEAN_DB_FROZEN": frozen,
            }

            with patch.dict("os.environ", test_envs):
                rb = RedBean(dsn=False)
            assert rb.config.frozen is False

    def test_setup(self):
        rb = RedBean(dsn=False)
        assert rb.config.dsn == "sqlite:////tmp/redbean.sqlite"

        rb = RedBean(dsn="sqlite:///abc.sqlite")
        assert rb.config.dsn == "sqlite:///abc.sqlite"

        rb = RedBean(dsn=False)
        assert rb.config.dsn == "sqlite:////tmp/redbean.sqlite"

        with pytest.raises(ConfigurationError):
            RedBean()
        with pytest.raises(ConfigurationError):
            RedBean(dsn="unknown://user:pass@localhost/dbname")

        with pytest.raises(sqlalchemy.exc.OperationalError):
            RedBean(dsn="postgresql+psycopg://user:pass@localhost/dbname")
        with pytest.raises(sqlalchemy.exc.OperationalError):
            RedBean(dsn="mysql+pymysql://user:pass@localhost/dbname")
