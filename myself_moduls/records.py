import json
import os


class Progress:
    """Класс для управления прогрессом игры (текущий уровень и рекорд).

    Сохраняет прогресс в JSON файл и обеспечивает его загрузку при старте.

    Attributes:
        record (int): Максимальный достигнутый уровень.
        current_lvl (int): Текущий уровень, на котором находится игрок.
        progress_file (str): Полный путь к файлу с сохранённым прогрессом.
    """

    def __init__(self, file_name="progress.json"):
        """Инициализирует менеджер прогресса.

        Args:
            file_name: Имя файла для сохранения прогресса
            (по умолчанию 'progress.json').
            Файл создаётся в той же директории, где находится этот модуль."""
        self.record = self.current_lvl = 1
        self.progress_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), file_name
        )
        self.load()

    def load(self):
        """Загружает сохранённый прогресс из файла.
        Если проблемы с файлом, создаётся новый с начальными значениями."""
        try:
            with open(self.progress_file, "r") as f:
                data = json.load(f)
                self.record = data.get("record", 1)
                self.current_lvl = data.get("current", 1)
        except Exception as e:
            print(f"Ошибка загрузки прогресса: {e}")
            self.save_progress()

    def save_progress(self):
        """Сохраняет текущий прогресс в файл."""
        try:
            with open(self.progress_file, "w", encoding="utf-8") as f:
                json.dump({"record": self.record,
                           "current": self.current_lvl}, f)
        except Exception as e:
            print(f"Ошибка сохранения прогресса: {e}")

    def new_level(self, win):
        """Обновляет прогресс после завершения уровня (победа или проигрыш).

        Args:
            win: True если игрок победил.
        """
        self.current_lvl = self.current_lvl + 1 if win else 1
        if self.current_lvl > self.record:
            self.record = self.current_lvl
        self.save_progress()

    def get_level(self):
        """Возвращает текущий уровень."""
        return self.current_lvl

    def get_record(self):
        """Возвращает рекорд."""
        return self.record
