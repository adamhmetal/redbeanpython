import os

from redbeanpython import Bean
from redbeanpython.cli.cli import main as cli_main
from tests.abstract import TestAbstract


class RedBeanCliTestAbstract(TestAbstract):
    @staticmethod
    def execute(cmd_args: list[str]):
        cli_main(cmd_args)

    def _create_test_entry(self, dsn: str, directory: str, namespace: str):
        rb = self.get_red_bean(
            dsn=dsn, namespace=namespace, directory=directory
        )
        rb.store(Bean(self.BEAN_TYPE, {"any": "any"}))
        assert os.path.exists(f"{directory}/models/test.py")
        assert os.path.exists(f"{directory}/migrations/env.py")

