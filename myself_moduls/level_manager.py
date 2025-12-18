from myself_moduls.get_absolute_path import get_path
import os


class LevelManager:
    """Менеджер уровней для игры. Управляет настройками и ресурсами уровней.

    Уровни 1-4 используют разные комбинации из 4 папок с изображениями.
    Уровни 5+ используют все 4 папки с модификаторами сложности.

    Attributes:
        dirs (tuple): Кортеж с именами папок изображений.
        base_levels (dict): Базовые конфигурации для первых 5 уровней.
        Ключ - номер базового уровня (1-5), значение - кортеж
            (названия папок картинок, время показа карточки, тип уровня).
        INITIAL_MOVES (int): Количество ходов для 1-го уровня.
        MOVES_DECREMENT (int): Шаг уменьшения ходов между базовыми уровнями.
    """

    def __init__(
        self,
        dirs=("images_1", "images_2", "images_3", "images_4"),
        custom_paths=None,
    ):
        """Инициализирует менеджер с базовыми настройками уровней.

        Args:
            dirs (tuple): Кортеж из 4 элементов с именами папок ресурсов.
                Можно передавать относительные имена папок
                (ищутся через get_path), которая ищет от корневой
                директории проекта. Убедитесь, что папки существуют в проекте.

        Raises:
            ValueError: Если длина кортежа dirs не 4.
        """
        self.dirs = dirs
        self.custom_paths = custom_paths if custom_paths else {}
        k = len(self.dirs)
        if k != 4:
            raise ValueError(
                f"Передаваемый кортеж должен "
                f"содержать 4 папки, получено: {k}"
            )

        self.base_levels = {
            1: ((dirs[0],), 1000, "normal"),
            2: (dirs[:2], 800, "normal"),
            3: (dirs[1:3], 700, "normal"),
            4: (dirs, 600, "normal"),
        }
        self.INITIAL_MOVES = 30
        self.MOVES_DECREMENT = 4

    def get_level(self, lvl_num: int):
        """Возвращает параметры для указанного уровня.

        Args:
            lvl_num (int): Номер уровня.

        Returns:
            Кортеж из:
            - moves: Количество ходов
            - paths: Список из полных путей к папкам с картинками
            - time: Время показа карточки в миллисекундах
            - lvl_type: Тип уровня

        Raises:
            ValueError: Если lvl_num < 1.
            FileNotFoundError: Если не удалось найти одну из папок ресурсов."""
        if lvl_num < 1:
            raise ValueError(
                f"Номер уровня должен быть >= 1, получен: {lvl_num}"
            )
        base_lvl = min(
            lvl_num, 4
        )  # Определяем базовый уровень (для всех уровней > 4 - 4)
        dir_names, time, lvl_type = self.base_levels[
            base_lvl
        ]  # Получаем базовую конфигурацию
        paths = []
        for dir_name in dir_names:
            if "images" in self.custom_paths:
                # Путь относительно пользовательской папки
                base_path = self.custom_paths["images"]
                if not os.path.isdir(base_path):
                    raise FileNotFoundError(
                        f"Папка с ресурсами не найдена: {base_path}"
                    )
                path = os.path.join(base_path, dir_name)
            else:
                path = get_path(dir_name)

            if not os.path.isdir(path):
                raise FileNotFoundError(
                    f"Папка с картинками не найдена: {path}"
                )

            paths.append(path)
        # Рассчитываем базовое кол-во ходов
        moves = self.INITIAL_MOVES - ((base_lvl - 1) * self.MOVES_DECREMENT)
        # Дополнительные модификации для уровней выше 4-го
        if lvl_num > 4:
            pos = (lvl_num - 5) % 4  # Циклическая позиция для вариаций
            # Модификация ходов (отклонения от базового кол-ва)
            moves = moves + [-1, -4, -1, +4][pos]
            types = ["normal", "ХАРДКОР!", "normal", "БОНУС!"]
            lvl_type = types[pos]
            # Особый уровень каждые 7 уровней (мало времени на показ карточек)
            if lvl_num % 7 == 0:
                time, lvl_type = 400, "СПРИНТ"
        moves, time = max(moves, 1), max(time, 100)
        return moves, paths, time, lvl_type
