import unittest
import os
import tempfile

from myself_moduls.make_list_images import list_files
from unittest.mock import patch, MagicMock


class TestListFilesSimple(unittest.TestCase):
    """Тесты для list_files."""

    def test_returns_16_cards(self):
        """Возвращает 16 карточек (8 пар)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            for i in range(8):
                file_path = os.path.join(temp_dir, f"img_{i}.png")
                open(file_path, "w").close()

            result = list_files((temp_dir,))
            self.assertEqual(len(result), 16)

    def test_each_image_has_pair(self):
        """У каждого изображения есть пара."""
        with tempfile.TemporaryDirectory() as temp_dir:
            files = []
            for i in range(8):
                path = os.path.join(temp_dir, f"pic_{i}.png")
                open(path, "w").close()
                files.append(path)
            result = list_files((temp_dir,))
            for path in files:
                count = result.count(path)
                self.assertEqual(count, 2)


class TestListFilesWithMocksSimple(unittest.TestCase):
    """Тесты с mock."""

    @patch("os.scandir")
    @patch("os.path.isdir")
    def test_mock_works(self, mock_isdir, mock_scandir):
        """Mock работает, функция вызывается и возвращает 16 файлов."""
        mock_isdir.return_value = True
        fake_files = []
        for i in range(8):
            mock_file = MagicMock()
            mock_file.is_file.return_value = True
            mock_file.name = f"img_{i}.png"
            mock_file.path = f"/test/img_{i}.png"
            fake_files.append(mock_file)

        mock_scandir.return_value = fake_files

        result = list_files(("/test",))
        self.assertEqual(len(result), 16)

    @patch("os.scandir")
    @patch("os.path.isdir")
    def test_error_when_not_enough_images(self, mock_isdir, mock_scandir):
        """Оошибка, если картинок меньше 8, и одновременно проверка,
        что не берутся файлы неверного формата."""
        mock_isdir.return_value = True

        files = []
        for i in range(5):
            mock_file = MagicMock()
            mock_file.is_file.return_value = True
            mock_file.name = f"img_{i}.png"
            mock_file.path = f"/test/img_{i}.png"
            files.append(mock_file)

        for i in range(10):
            mock_file = MagicMock()
            mock_file.is_file.return_value = True
            mock_file.name = f"other_{i}.txt"
            mock_file.path = f"/test/other_{i}.txt"
            files.append(mock_file)

        mock_scandir.return_value = files

        with self.assertRaises(FileNotFoundError) as context:
            list_files(("/test",))

        error_msg = str(context.exception)
        self.assertIn("Недостаточно", error_msg)


if __name__ == "__main__":
    unittest.main()
