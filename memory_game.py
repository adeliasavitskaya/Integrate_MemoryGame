"""
Главный модуль игры на память (Memory Game).

Игра в карточки, где нужно находить пары одинаковых изображений.
Управляет игровым процессом, уровнями, звуками и интерфейсом.
"""
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QColor

from myself_moduls.square_window import make_window_square
from myself_moduls.make_list_images import list_files
from myself_moduls.dialogs import GameResultDialog, SettingsDialog
from myself_moduls.records import Progress
from myself_moduls.music_and_sounds_manager import MusicManager, SoundManager
from myself_moduls.level_manager import LevelManager
from myself_moduls.get_absolute_path import get_path

class MemoryGame(QMainWindow):
    """Главное окно игры Memory Game.

            Attributes:
                level_manager (LevelManager): Управляет уровнями игры.
                sounds (SoundManager): Управляет звуковыми эффектами.
                music (MusicManager): Управляет фоновой музыкой.
                progress (Progress): Управляет прогрессом игрока.
                current_lvl (int): Текущий уровень игры.
                record (int): Рекорд игрока.
                moves_count (int): Оставшееся количество ходов.
                time_show (int): Время показа карточек в миллисекундах.
                images (list): Список путей к изображениям для карточек.
                cards (list): Список кнопок-карточек.
                card_states (dict): Состояние каждой карточки.
                turned_cards (list): Индексы перевернутых карточек.
                is_checking (bool): Флаг, ведется ли проверка совпадения карточек.
            """
    def __init__(self, custom_paths=None):
        """Инициализирует главное окно игры."""
        super().__init__()
        self.custom_paths = custom_paths if custom_paths else {}
        self._load_ui()
        self._init_all_game()

        self.turned_cards = []
        self.is_checking = False

    def _load_ui(self):
        """Загружает интерфейс из файла .ui."""
        try:
            ui_name = 'game.ui'
            ui_path = self.custom_paths.get('ui') or get_path(ui_name)
            uic.loadUi(ui_path, self)
        except Exception as e:
            print(f"Ошибка загрузки UI: {e}")
            sys.exit(1)

    def _init_all_game(self):
        """Настраивает все компоненты игры."""
        self._init_managers()
        self._init_level()
        self._init_cards()
        self._set_card_states()
        self._interfaces_buttons_clicked()

    def _init_managers(self):
        """Инициализирует менеджеры звука, музыки и уровней."""
        self.level_manager = LevelManager(custom_paths=self.custom_paths)
        try:
            self.sounds = SoundManager(custom_paths=self.custom_paths)
        except Exception as e:
            print(f"Звуки не загружены: {e}")
            self.sounds = None

        try:
            self.music = MusicManager(custom_paths=self.custom_paths)
            if self.music.load("music.ogg"):
                self.music.play()
        except Exception as e:
            print(f"Музыка не загружена: {e}")
            self.music = None

    def _init_level(self):
        """Инициализирует текущий уровень игры."""
        try:
            self.progress = Progress()
            self.current_lvl = self.progress.get_level()
            self.record = self.progress.get_record()
            lvl_info = self.level_manager.get_level(self.current_lvl)
            self.moves_count, dir_paths, self.time_show, lvl_type = lvl_info
            self.images = list_files(dir_paths)
        except Exception as e:
            print(f"Ошибка инициализации уровня, используем тестовые данные: {e}")
            self._use_test_data()
        self._set_ui_levels()

    def _use_test_data(self):
        """Использует тестовые данные при ошибке."""
        self.record = self.current_lvl = 1
        self.moves_count, self.time_show = 30, 1000
        from random import shuffle
        test_pairs = [f'{x}.png' for x in range(8)] * 2
        shuffle(test_pairs)
        self.images = test_pairs

    def _set_ui_levels(self):
        """Обновляет информацию об уровне в интерфейсе."""
        try:
            passed_lvl, passed_rec = self.current_lvl-1, self.record-1
            self.passed_lvl_label.setText(f'🏆 {passed_lvl}')
            self.record_label.setText(f'🏆 {passed_rec}')
            self.moves_label.setText(f'ХОДЫ\t{self.moves_count}')
        except AttributeError as e:
            print(f"Не найден нужный QLabel в UI: {e}")

    def _init_cards(self):
        """Инициализирует карточки игры.

        Находит все кнопки карточек, настраивает их внешний вид
        и подключает обработчики кликов."""
        try:
            self.cards = sorted([btn for btn in self.findChildren(QPushButton)
                                 if 'card_' in btn.objectName()],
                                key=lambda btn: btn.objectName())
            if not self.cards: raise ValueError("Карточки не найдены")

            def create_click_handler_for_card(idx):
                """Создаёт новый обработчик клика для каждой карточки"""
                return lambda: self.press_card(idx)

            for i, card in enumerate(self.cards):
                card.clicked.connect(create_click_handler_for_card(i))

                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(30)
                shadow.setXOffset(10)
                shadow.setYOffset(10)
                shadow.setColor(QColor(120, 110, 140, 60))
                card.setGraphicsEffect(shadow)
        except Exception as e:
            print(f"Критическая ошибка: {e}! Не могу создать карточки")
            sys.exit(1)

    def _set_card_states(self):
        """Устанавливает начальные состояния для всех карточек."""
        self.card_states = {
        i: {'card': card, 'img': self.images[i], 'turned_over': False, 'found_pair': False, 'icon': None}
        for i, card in enumerate(self.cards)}

    def _interfaces_buttons_clicked(self):
        """Подключает обработчики кликов к кнопкам интерфейса."""
        try:
            restart_icon = self.custom_paths.get('restart_icon')
            menu_icon = self.custom_paths.get('menu_icon')
            self.reboot.setIcon(QIcon(restart_icon if restart_icon else get_path('restart.png')))
            self.menu.setIcon(QIcon(menu_icon if menu_icon else get_path('menu.png')))

            from myself_moduls.square_window import update_icon_size
            update_icon_size([self.reboot, self.menu], percent=0.7)
            self.reboot.clicked.connect(self.restart)
            self.menu.clicked.connect(self.show_settings)
        except AttributeError as e:
            print(f"Кнопка не найдена в UI: {e}")

    def resizeEvent(self, event):
        """Обработчик изменения размера окна.
        Обеспечивает квадратную форму окна и обновляет размер иконок карточек."""
        try:
            super().resizeEvent(event)
            make_window_square(self, cards=self.cards)
        except Exception as e:
            print(f"Ошибка при изменении размера окна: {e}")

    def press_card(self, index_card):
        """Обрабатывает нажатие на карточку.

        Args:
            index_card: Индекс нажатой карточки."""
        try:
            if self.can_turn(index_card):
                self.flip_card(index_card, self.card_states[index_card]['img'])
                self.turned_cards.append(index_card)
                if len(self.turned_cards) == 2: # Если перевернуто 2 карточки, проверяем совпадение
                    self.check_match()
        except Exception as e:
            print(f" Ошибка при нажатии на карточку: {e}")

    def can_turn(self, index_card):
        """Проверяет можно ли перевернуть карточку.

        Args:
            index_card: Индекс карточки.

        Returns:
            bool: True если карточку можно перевернуть."""
        try:
            card_state = self.card_states[index_card]
            # Нельзя перевернуть если:
            # 1. Карточка уже найдена в паре
            # 2. Карточка уже перевернута
            # 3. Уже перевернуто 2 карточки для проверки
            # 4. Идёт проверка совпадения
            return (not card_state['found_pair'] and not card_state['turned_over']
                    and len(self.turned_cards) < 2 and
                    not self.is_checking)
        except KeyError:
            print(f"Несуществующий индекс карточки: {index_card}")
            return False
        except Exception as e:
            print(f"Ошибка проверки возможности переворота: {e}")
            return False

    def check_match(self):
        """Проверяет совпадение перевернутых карточек."""
        try:
            self.is_checking = True
            index_1, index_2 = self.turned_cards
            # результат проверки на совпадение
            bool_match_pair = (self.card_states[index_1]['img'] == self.card_states[index_2]['img'])
            self.process_match(index_1, index_2, match=bool_match_pair, time=self.time_show)
        except Exception as e:
            print(f"Ошибка проверки совпадения: {e}")
            self.turned_cards.clear()
            self.is_checking = False

    def process_match(self, index_1, index_2, match, time=1000):
        """Обрабатывает результат проверки совпадения карточек.

        Args:
            index_1: Индекс первой карточки.
            index_2: Индекс второй карточки.
            match: результат проверки на совпадение, True если совпадают.
            time: Время задержки перед скрытием карточек."""
        try:
            if not match:
                self.moves_count -= 1 # Не совпали, тратим ход
                self.moves_label.setText(f'ХОДЫ\t{self.moves_count}')
                QTimer.singleShot(time, lambda: self.hide_cards(index_1, index_2))
            else:
                if self.sounds: self.sounds.play_param('match')
                for i in (index_1, index_2):
                    self._effect_for_matched_cards(i)
                    self.card_states[i]['found_pair'] = True
                self.turned_cards.clear()
                self.is_checking = False
            self.check_game_completion() # Проверяем завершение игры
        except Exception as e:
            print(f"Ошибка обработки совпадения: {e}")
            self.turned_cards.clear()
            self.is_checking = False

    def _effect_for_matched_cards(self, index_card):
        """Добавляет визуальный эффект для найденной пары.

        Args:
            index_card: Индекс карточки."""
        try:
            card = self.card_states[index_card]['card']
            checkmark = QLabel('✓︎', card)
            checkmark.setStyleSheet('''
                QLabel {
                    color: #32CD32;
                    font-size: 64px;
                    font-weight: bold;
                    background: transparent;}''')
            checkmark.setAlignment(Qt.AlignCenter)
            checkmark.setGeometry(0, 0, card.width(), card.height())
            checkmark.show()
            QTimer.singleShot(1000, checkmark.deleteLater)
        except Exception as e:
            print(f"Ошибка создания визуального эффекта: {e}")

    def flip_card(self, index_card, img=''):
        """Переворачивает карточку.

        Args:
            index_card: Индекс карточки.
            img: Путь к изображению для показа (пустая строка, когда надо скрыть)."""
        try:
            if self.sounds: self.sounds.play_param('flip')
            card_state = self.card_states[index_card]
            card = card_state['card']

            card.hide()
            QTimer.singleShot(200, card.show)

            card.setIcon(QIcon(img))
            card_state['turned_over'] = bool(img)
        except Exception as e:
            print(f"Ошибка переворота карточки: {e}")

    def hide_cards(self, index_1, index_2):
        """Скрывает несовпавшие карточки.

        Args:
            index_1: Индекс первой карточки.
            index_2: Индекс второй карточки."""
        try:
            for i in (index_1, index_2):
                self._hide_single_card_with_visual(i)
        except Exception as e:
            print(f"Ошибка скрытия карточек: {e}")
        self.turned_cards.clear()
        self.is_checking = False

    def _hide_single_card_with_visual(self, index_card):
        """Скрывает одну карточку с анимацией.

        Args:
            index_card: Индекс карточки."""
        try:
            card = self.card_states[index_card]['card']
            self.flip_card(index_card)
            card.hide()
            QTimer.singleShot(150, card.show)
        except Exception as e:
            print(f"Ошибка скрытия карточки: {e}")

    def check_game_completion(self):
        """ Проверяет условия завершения игры после каждого хода.
        Вызывается после обработки пары (совпадения или нет)"""
        try:
            # Проверяем победу (все пары найдены)
            if all(state['found_pair'] for state in self.card_states.values()):
                self.game_completion(win=True)
            # Проверяем поражение (закончились ходы)
            elif self.moves_count <= 0:
                self.game_completion(win=False)
        except Exception as e:
            print(f"Ошибка проверки завершения игры: {e}")

    def game_completion(self, win=False):
        """Завершает игру с указанным результатом.

        Args:
            win: True, если игрок победил."""
        try:
            self.show_game_result(win)
        except Exception as e:
            print(f"Ошибка завершения игры: {e}")

    def restart(self):
        """Перезапускает игру."""
        try:
            self.start_next_game(win=False)
        except Exception as e:
            print(f"Ошибка перезапуска игры: {e}")

    def start_next_game(self, win):
        """Начинает следующую игру.

        Args:
            win: True если игрок победил в предыдущей игре."""
        try:
            # добавляем в прогресс информацию
            # (если win, начнем следующий уровень, иначе перезапуск)
            self.progress.new_level(win)
            self.reset_level()
        except Exception as e:
            print(f"Ошибка начала игры: {e}")

    def reset_level(self):
        """Начальное состояние карточек и интерфейса для нового уровня. (следующего или 1-го)"""
        try:
            self._init_level()
            self._set_card_states()
            self._reset_ui_cards()
        except Exception as e:
            print(f"Ошибка сброса уровня: {e}")

    def _reset_ui_cards(self):
        """Сбрасывает иконки всех карточек."""
        for card in self.cards:
            try:
                card.setIcon(QIcon())
            except Exception as e:
                print(f"Ошибка сброса карточки: {e}")

    def show_game_result(self, win):
        """Показывает диалог с результатом игры.

        Args:
            win: True если игрок победил."""
        try:
            dialog = GameResultDialog(win=win, sounds=self.sounds, parent=self)
            dialog.exec_()
        except Exception as e:
            print(f"Ошибка показа диалога результата: {e}")

    def show_settings(self):
        """Показывает диалог настроек."""
        try:
            dialog = SettingsDialog(music_manager=self.music,
                                    sound_manager=self.sounds, parent=self)
            dialog.exec_()
        except Exception as e:
            print(f"Ошибка показа диалога настроек: {e}")
