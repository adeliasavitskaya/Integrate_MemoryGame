"""
Точка входа для запуска Memory Game.

Игра в карточки на память с графическим интерфейсом на PyQt5.

Запуск:
    python main.py  # стандартные ресурсы

Для использования пользовательских ресурсов (пример кода):
    custom_paths = {
        'ui': './my_ui/game.ui', главный ui файл программы
        'images': './my_images/', путь к папке, в которой содержатся 4 папки изображений
        с именами images_1, images_2, images_3, ...
        'music': './sounds/my_music.ogg', музыка
        'sound_flip': './sounds/flip.wav', звук переворота карточек
        'sound_match': './sounds/match.wav', звук для найденных пар
        'sound_win': './sounds/win.wav', звук победы
        'sound_lose': './sounds/lose.wav', звук поражения
        'restart_icon': './icons/restart.png', изображение для кнопки перезагрузки
        'menu_icon': './icons/menu.png' изображение для кнопки настроек
    }
    game = MemoryGame(custom_paths=custom_paths)
"""

import sys
from PyQt5.QtWidgets import QApplication
from memory_game import MemoryGame


def main():
    """Основная функция запуска приложения."""
    try:
        # Пустой словарь - используем стандартные ресурсы
        custom_paths = {}

        app = QApplication(sys.argv)
        game = MemoryGame(custom_paths=custom_paths)
        game.show()
        app.exec_()

    except Exception as e:
        print(f"Ошибка запуска: {e}")


if __name__ == '__main__':
    main()