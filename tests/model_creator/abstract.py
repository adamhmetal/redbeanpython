import datadiff

from tests.abstract import TestAbstract


class ModelCreatorTestAbstract(TestAbstract):
    @staticmethod
    def assert_model_equals(expected_file, got_file):
        with open(f"tests/resources/models/{expected_file}") as f:
            expected_content = f.read()
        with open(got_file) as f:
            given_content = f.read()

        assert expected_content == given_content, datadiff.diff(
            given_content,
            expected_content,
        )
