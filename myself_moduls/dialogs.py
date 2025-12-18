from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from myself_moduls.get_absolute_path import get_path

def set_center_geometry(window, parent):
    """Помещает окно в центр родительского окна.

    Args:
        window: Окно для позиционирования.
        parent: Родительское окно.
    """
    window.move(parent.geometry().center() - window.rect().center())


class GameResultDialog(QDialog):
    """Диалоговое окно с результатом игры"""
    def __init__(self, win=True, sounds=None, parent=None):
        """Инициализирует диалог результата игры.

        Args:
            win: True для победы, False для поражения.
            sounds: Менеджер звуков для воспроизведения.
            parent: Родительское окно.
        """
        super().__init__(parent, Qt.WindowType(Qt.FramelessWindowHint))
        try:
            uic.loadUi(get_path('game_result.ui'), self)
            sounds.play_param('win' if win else 'lose')
            if parent: set_center_geometry(self, parent)
            self._init_result_config()
            self.result_ui(win)
            if parent: self.btn_play.clicked.connect(lambda: self.close_window(win))
        except FileNotFoundError as e:
            print(f"Файл интерфейса не найден: {e}")
        except Exception as e:
            print(f"Ошибка создания диалога: {e}")

    def _init_result_config(self):
        """Создает конфигурацию для разных результатов."""
        self.configs = {
            'win': {'icon': get_path('win.png'), 'title': 'ПОБЕДА',
                    'message': 'Хотите продолжить игру?',
                    'button': get_path('next_lvl.png')},
            'lose': {'icon': get_path('lose.png'), 'title': 'ПОРАЖЕНИЕ',
                     'message': 'Ходы закончились!',
                     'button': get_path('restart.png')}}

    def result_ui(self, win):
        """Настраивает интерфейс в зависимости от результата.

        Args:
            win: True для победы, False для поражения.
        """
        try:
            cfg = self.configs['win' if win else 'lose']
            self.icon_label.setPixmap(QIcon(cfg['icon']).pixmap(100, 100))
            self.title_label.setText(cfg['title'])
            self.message_label.setText(cfg['message'])
            self.btn_play.setIcon(QIcon(cfg['button']))
            self.btn_play.setIconSize(self.btn_play.size() * 0.8)
        except Exception as e:
            print(f"Ошибка настройки интерфейса: {e}")

    def close_window(self, win):
        """Закрывает диалог и запускает следующую игру.

        Args:
            win: True если игрок победил.
        """
        try:
            self.accept()
            if self.parent(): self.parent().start_next_game(win)
        except Exception as e:
            self.accept()
            print(f"Ошибка запуска  диалога: {e}")


class SettingsDialog(QDialog):
    """Диалоговое окно настроек (звук, музыка)."""
    def __init__(self, music_manager=None, sound_manager=None, parent=None):
        """Инициализирует диалог настроек.

        Args:
            music_manager: Менеджер музыки.
            sound_manager: Менеджер звуков.
            parent: Родительское окно.
        """
        super().__init__(parent, Qt.WindowType(Qt.FramelessWindowHint))
        try:
            uic.loadUi(get_path('settings.ui'), self)
            if parent: set_center_geometry(self, parent)
            self.music = music_manager
            self.sound = sound_manager

            self.chck_music.setChecked(self.music.playing)
            self.chck_sounds.setChecked(self.sound.playing)

            self.chck_music.toggled.connect(self.music_changed)
            self.chck_sounds.toggled.connect(self.sounds_changed)
            self.close_btn.clicked.connect(self.accept)
        except FileNotFoundError as e:
            print(f"Файл настроек не найден: {e}")
        except Exception as e:
            print(f"Ошибка создания диалога настроек: {e}")

    def music_changed(self, is_on):
        """Обрабатывает изменение состояния музыки.

        Args:
            is_on: True чтобы включить музыку, False чтобы выключить.
        """
        try:
            if self.music:
                if is_on:
                    self.music.play()
                else:
                    self.music.pause()
        except Exception as e:
            print(f"Ошибка изменения состояния музыки: {e}")

    def sounds_changed(self, is_on):
        """Обрабатывает изменение состояния звуковых эффектов.

        Args:
            is_on: True чтобы включить звуки, False чтобы выключить.
        """
        try:
            if self.sound: self.sound.playing = True if is_on else False
        except Exception as e:
            print(f"Ошибка изменения состояния звуковых эффектов: {e}")