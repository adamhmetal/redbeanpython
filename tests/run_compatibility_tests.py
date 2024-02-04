import os
import subprocess
import sys

from colored import stylize, fore

PYTHON_VERSIONS = [
    "3.12",
    "3.11",
]

PACKAGES_VERSIONS = {
    "latest (2024)": [
        "SQLAlchemy==2.0.25",
        "psycopg==3.1.17",
        "PyMySQL==1.1.0",
        "alembic==1.13.1",
    ],
    "legacy (2022)": [
        "SQLAlchemy==2.0.0",
        "psycopg==3.0.18",
        "PyMySQL==1.0.2",
        "alembic==1.8.0",
    ],
}

DATABASES = {
    "postgres": [
        "postgres:16.1",
        "postgres:9.0.23",
    ],
    "mysql": [
        "mysql:8.3.0",
        "mysql:8.0.0",
        "mariadb:11.2.2",
        "mariadb:10.4.0",
    ],
    "sqlite": [
        "build-in",
    ],
}


class _SummaryRow:
    def __init__(
        self,
        *,
        python_version: str,
        db: str,
        db_version: str,
        packages_label: str,
        packages: list[str],
        passed: bool,
    ):
        self.python_v = python_version
        self.db = db
        self.db_v = db_version
        self.packages = packages
        self.packages_label = packages_label
        self.passed = passed

    def __str__(self):
        msg = ":material-check: OK" if self.passed else ":material-close: FAILED"
        result = stylize(msg, fore("green") if self.passed else fore("red"))
        return f"| {self.db} ({self.db_v}) | {self.python_v} | {self.packages_label} {self.packages} | {result} |"


def run_compatibility_tests():
    summary = []
    execution_status = True
    for db, db_versions in DATABASES.items():
        for db_version in db_versions:
            for python_version in PYTHON_VERSIONS:
                for package_version, packages in PACKAGES_VERSIONS.items():
                    install_dependencies_command = ""
                    for package in packages:
                        install_dependencies_command += f"poetry add {package} &&"

                    command = [
                        "docker",
                        "compose",
                        "-f",
                        "tests/docker/docker-compose.yml",
                        "run",
                        "--build",
                        "--rm",
                        "--service-ports",
                        "--entrypoint",
                        f"bash -c '{install_dependencies_command} poetry run poe test'",
                        f"package-{db}",
                    ]

                    print(
                        f"Running tests for: {db} ({db_version}) python: {python_version} package_version {packages}"
                    )
                    print(f"Command: {' '.join(command)}")

                    my_env = os.environ.copy()
                    my_env["PYTHON_VERSION"] = python_version
                    my_env["DATABASE_VERSION"] = db_version
                    my_env["DATABASE"] = db

                    process = subprocess.run(command, env=my_env)
                    test_status = process.returncode == 0
                    summary.append(
                        _SummaryRow(
                            python_version=python_version,
                            db=db,
                            db_version=db_version,
                            packages_label=package_version,
                            packages=packages,
                            passed=test_status,
                        )
                    )

                    execution_status = execution_status and test_status

    print("| database | python | packages | status |")
    print("|----------|--------|----------|--------|")
    for row in summary:
        print(row)

    sys.exit(0 if execution_status else 1)
