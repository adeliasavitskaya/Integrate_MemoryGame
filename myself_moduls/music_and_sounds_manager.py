from myself_moduls.get_absolute_path import get_path
import pygame


class SoundManager:
    """Менеджер звуковых эффектов игры.

    Управляет воспроизведением звуков: переворот карты, совпадение,
    победа, поражение.

    Attributes:
        playing (bool): Флаг включения/выключения звуков.
        sounds (Dict[str, pygame.mixer.Sound]): Словарь загруженных звуков.
    """

    def __init__(self, custom_paths=None):
        """Инициализирует менеджер звуков и загружает звуковые файлы."""
        self.playing = True
        self.custom_paths = custom_paths if custom_paths else {}
        try:
            pygame.mixer.init()
            sound_names = ("flip", "match", "win", "lose")
            self.sounds = {}
            for name in sound_names:
                custom_sound = self.custom_paths.get(f"sound_{name}")
                if custom_sound:
                    path = custom_sound
                else:
                    path = get_path(f"{name}.wav")

                self.sounds[name] = pygame.mixer.Sound(path)
        except Exception as e:
            print(f"Ошибка загрузки звуков: {e}")

    def play_param(self, param):
        """Воспроизводит звук по его имени.

        Args:
            param: Имя звука ('flip', 'match', 'win', 'lose')
        """
        if not self.playing:
            return

        if param not in self.sounds:
            print(
                f"Звук '{param}' не найден. "
                f"Доступные: {list(self.sounds.keys())}")
            return

        try:
            self.sounds[param].play()
        except Exception as e:
            print(f"Ошибка воспроизведения звука '{param}': {e}")


class MusicManager:
    """Менеджер фоновой музыки в игре.

    Обеспечивает загрузку, воспроизведение и управление фоновой музыкой
    с использованием библиотеки Pygame mixer.

    Attributes:
        playing (bool): Флаг, указывающий играет ли музыка в данный момент.
        loaded (bool): Флаг, указывающий успешно ли загружен музыкальный файл.
    """

    def __init__(self, custom_paths=None):
        """Инициализирует менеджер музыки и звуковую систему Pygame."""
        self.playing = False
        self.loaded = False
        self.custom_paths = custom_paths if custom_paths else {}
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Ошибка инициализации музыки: {e}")

    def load(self, filename="music.ogg", volume=0.5):
        """Загружает музыкальный файл.
        По умолчанию используется музыка в формате OGG

        Args:
            filename: Имя музыкального файла. Должен находиться в корне проекта
                     или доступных для поиска директориях.
            volume: Уровень громкости. По умолчанию 0.5.
        """
        try:
            custom_music = self.custom_paths.get("music")
            music_path = custom_music if custom_music else get_path(filename)

            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            self.loaded = True
            return True
        except Exception as e:
            print(f"Ошибка загрузки музыки: {e}")
            return False

    def play(self):
        """Включает музыку
        Если музыка уже играет, метод ничего не делает.
        Музыка воспроизводится в бесконечном цикле (-1)."""
        if self.loaded and not self.playing:
            try:
                pygame.mixer.music.play(-1)
                self.playing = True
            except Exception as e:
                print(f"Ошибка воспроизведения музыки: {e}")

    def pause(self):
        """Останавливает воспроизведение музыки.
        Музыку можно возобновить вызовом play()."""
        if self.playing:
            try:
                pygame.mixer.music.pause()
                self.playing = False
            except Exception as e:
                print(f"Ошибка паузы музыки: {e}")
