import unittest
import os

from myself_moduls.get_absolute_path import get_path, find_project_root


class TestGetPath(unittest.TestCase):
    """Простые тесты для проверки нахождения пути к файлу или папке."""

    def test_find_project_root(self):
        """Тест 1: find_project_root находит корень проекта."""
        root = find_project_root()

        self.assertTrue(os.path.exists(root))
        self.assertTrue(os.path.isdir(root))

        files_in_root = os.listdir(root)
        has_project_marker = any(
            f in files_in_root
            for f in ["README.md", "requirements.txt",
                      ".git", "pyproject.toml"])

        self.assertTrue(has_project_marker)

    def test_get_path_finds_file(self):
        """Тест 2: get_path находит существующий файл."""
        test_files = ["requirements.txt", "main.py", "memory_game.py"]

        for filename in test_files:
            try:
                path = get_path(filename)
                if os.path.exists(path):
                    # Успех - проверяем что путь содержит имя файла
                    self.assertIn(filename, path)
                    return  # Успех, выходим
            except FileNotFoundError:
                continue

        self.fail(f"Не найден ни один файл из {test_files}")

    def test_get_path_empty_name_error(self):
        """Тест 3: get_path ошибка для пустого имени."""
        with self.assertRaises(ValueError):
            get_path("")

    def test_get_path_nonexistent_error(self):
        """Тест 4: get_path ошибка для несуществующего файла."""
        fake_file = "non_file.png"
        with self.assertRaises(FileNotFoundError) as context:
            get_path(fake_file)
        error_msg = str(context.exception)
        self.assertIn(fake_file, error_msg)

    def test_path_is_absolute(self):
        """Возвращает абсолютный путь."""
        path = get_path("requirements.txt")
        self.assertTrue(os.path.isabs(path))


if __name__ == "__main__":
    unittest.main()
