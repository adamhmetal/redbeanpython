import os
import sys
import tempfile

from redbeanpython.const import MODULE_NAME
from redbeanpython.errors import ConfigurationError
from redbeanpython.errors import NotExistsError


class Config:
    def __init__(self, dsn: str, frozen: bool, directory: str, namespace: str):
        self._dsn = dsn or self._get_dsn_default(dsn)
        self._frozen = frozen or self._get_frozen_default()
        self._namespace = namespace or self._get_namespace_default()
        self._directory = self._get_real_path(directory)

        self._validate_dsn()
        self._validate_directory()

    @property
    def dsn(self) -> str:
        return self._dsn

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def directory(self) -> str:
        return self._directory

    @property
    def models_directory(self) -> str:
        return os.path.join(self.directory, "models")

    @property
    def migrations_directory(self) -> str:
        return os.path.join(self.directory, "migrations")

    def _validate_dsn(self):
        dsn_driver = self.dsn.split(":")[0]
        if dsn_driver not in ["sqlite", "mysql+pymysql", "postgresql+psycopg"]:
            raise ConfigurationError(
                f"Unsupported driver: {dsn_driver}. Supported: 'sqlite', 'mysql+pymysql', 'postgresql+psycopg'"
            )

    def _validate_directory(self):
        if self.frozen and not os.path.exists(self.models_directory):
            raise NotExistsError(f"Models dir {self.models_directory} does not exist")

    @staticmethod
    def _get_real_path(directory: str) -> str:
        root_dir = os.path.dirname(sys.modules["__main__"].__file__)
        directory = directory or os.environ.get("REDBEAN_DIRECTORY", MODULE_NAME)
        return os.path.join(os.path.realpath(root_dir), directory)

    @staticmethod
    def _get_dsn_default(dsn: bool | str | None) -> str:
        if "REDBEAN_DB_DSN" in os.environ:
            return os.environ["REDBEAN_DB_DSN"]
        if dsn is False:
            return f"sqlite:///{tempfile.gettempdir()}/redbean.sqlite"
        raise ConfigurationError("Dsn is not provided. Use setup('...dsn...') or set REDBEAN_DB_DSN env var")

    @staticmethod
    def _get_frozen_default() -> bool:
        if "REDBEAN_DB_FROZEN" not in os.environ:
            return False
        if os.environ.get("REDBEAN_DB_FROZEN", "True").lower() in ["false", "0", "no"]:
            return False
        return True

    @staticmethod
    def _get_namespace_default() -> str:
        return os.environ.get("REDBEAN_NAMESPACE", MODULE_NAME)
