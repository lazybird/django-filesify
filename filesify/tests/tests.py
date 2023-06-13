import pathlib

from django.test import TestCase

from filesify.tests.models import MyConfigModel


class TestIsFileMixin:
    def assertIsFile(self, path):
        if not pathlib.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))


class FilesifyModelsTestCase(TestIsFileMixin, TestCase):
    def setUp(self):
        self.my_config = MyConfigModel(
            file_path="/tmp/example.txt", file_content="Hello, World!"
        )

    def test_model_is_created(self):
        self.assertEqual(self.my_config.file_path, "/tmp/example.txt")
        self.assertEqual(self.my_config.file_content, "Hello, World!")

    def test_file_is_created(self):
        file_path = pathlib.Path(self.my_config.file_path)
        self.assertIsFile(file_path)
