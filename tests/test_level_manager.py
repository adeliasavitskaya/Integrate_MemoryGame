"""Тесты для LevelManager"""

import unittest
from myself_moduls.level_manager import LevelManager


class TestLevelManagerSimple(unittest.TestCase):
    """Тесты для проверки LevelManager."""

    def test_level_1(self):
        """Тест 1: Уровень 1 возвращает правильные настройки."""
        manager = LevelManager()

        moves, paths, time, lvl_type = manager.get_level(1)

        self.assertEqual(
            (moves, time, lvl_type, len(paths)), (30, 1000, "normal", 1)
        )

    def test_level_4(self):
        """Тест 2: Уровень 4 работает правильно."""
        manager = LevelManager()

        moves, paths, time, lvl_type = manager.get_level(4)

        # Уровень 4: 30 - ((4-1)*4) = 30 - 12 = 18 ходов
        self.assertEqual(
            (moves, time, lvl_type, len(paths)), (18, 600, "normal", 4)
        )

    def test_level_5(self):
        """Тест 3: Уровень 5 использует базу от 4 уровня."""
        manager = LevelManager()

        moves, paths, time, lvl_type = manager.get_level(5)

        # Уровень 5: база от уровня 4 (18 ходов) + [-1, -4, -1, +4][0] = 17
        self.assertEqual(
            (moves, time, lvl_type, len(paths)), (17, 600, "normal", 4)
        )

    def test_level_6_hardcore(self):
        """Тест 4: Проверка, что уровень 6 имеет тип ХАРДКОР!."""
        manager = LevelManager()

        moves, paths, time, lvl_type = manager.get_level(6)

        # Уровень 6: база 18 + [-1, -4, -1, +4][1] = 18 - 4 = 14
        self.assertEqual(
            (moves, time, lvl_type, len(paths)), (14, 600, "ХАРДКОР!", 4)
        )

    def test_level_8_bonus(self):
        """Тест 5: Уровень 8 - БОНУС!."""
        manager = LevelManager()

        moves, paths, time, lvl_type = manager.get_level(8)

        # Уровень 8: база 18 + [-1, -4, -1, +4][3] = 18 + 4 = 22
        self.assertEqual(
            (moves, time, lvl_type, len(paths)), (22, 600, "БОНУС!", 4)
        )

    def test_6_level_14_sprint_check(self):
        """Тест 6: Уровень 7 должен иметь время 400 мс (каждый 7-й)."""
        manager = LevelManager()

        moves, paths, time, lvl_type = manager.get_level(14)

        # Уровень 7: кратен 7, поэтому время должно быть 400
        self.assertEqual(time, 400)
        self.assertEqual(lvl_type, "СПРИНТ")

    def test_level_0_error(self):
        """Тест 7: Уровень 0 вызывает ошибку."""
        manager = LevelManager()

        with self.assertRaises(ValueError) as context:
            manager.get_level(0)

        error_msg = str(context.exception)
        self.assertIn(">= 1", error_msg)

    def test_level_negative_error(self):
        """Тест 8: Отрицательный уровень вызывает ошибку."""
        manager = LevelManager()

        with self.assertRaises(ValueError):
            manager.get_level(-3)


if __name__ == "__main__":
    unittest.main()
