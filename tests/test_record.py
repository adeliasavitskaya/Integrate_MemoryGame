import unittest
import tempfile
import os
import json

from myself_moduls.records import Progress


class TestProgress(unittest.TestCase):
    """Тесты для проверки корректности сохранения
    и получения прогресса в игре."""

    def test_base_changes(self):
        """Тесты ведутся во временной папке."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, "progress.json")

            with open(test_file, "w") as f:
                json.dump({"record": 1, "current": 1}, f)

            game = Progress(file_name=test_file)

            self.assertEqual(game.get_level(), 1)
            self.assertEqual(game.get_record(), 1)

            game.new_level(win=True)
            self.assertEqual(game.get_level(), 2)
            self.assertEqual(game.get_record(), 2)

            game.new_level(win=False)
            self.assertEqual(game.get_level(), 1)
            self.assertEqual(game.get_record(), 2)

    def test_file_gets_created(self):
        """Проверка, что файл создается в текущей папке."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, "new_progress.json")
            self.assertFalse(os.path.exists(test_file))
            Progress(file_name=test_file)
            self.assertTrue(os.path.exists(test_file))


if __name__ == "__main__":
    unittest.main()
