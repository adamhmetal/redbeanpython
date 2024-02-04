import shutil

from redbeanpython.redbean import RedBean


class StoreTestDataAsResourceUtil:
    def __init__(self, rb: RedBean):
        self.redbean = rb

    def store_models(self, destination_dir: str):
        shutil.copytree(self.redbean._directory, destination_dir)

    def store_migrations(self, destination_dir: str):
        shutil.copytree(
            f"{self.redbean._directory}/migrations", f"{destination_dir}/migrations"
        )
