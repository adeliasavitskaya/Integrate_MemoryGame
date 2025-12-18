from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QPushButton

def make_window_square(window, cards=None):
    """
    Устанавливает обработчик события изменения размера, который поддерживает
    квадратную форму окна. При необходимости обновляет размер иконок на кнопках.

    Args:
        window: Окно, которое нужно сделать квадратным. Экземпляр QWidget.
        cards: Список кнопок (QPushButton), у которых нужно обновлять
               размер иконок при изменении размера окна, если не None.

    Raises:
        TypeError: Если window не является экземпляром QWidget.
        TypeError: Если cards не None и не список.
    """
    if not isinstance(window, QWidget):
        raise TypeError(f"window должен быть экземпляром QWidget")
    if cards is not None and not isinstance(cards, list):
        raise TypeError(f"cards должен быть списком, получен {type(cards)}")

    original_resize = window.resizeEvent

    def square_resize(event):
        """Обработчик события изменения размера окна."""
        try:
            size = min(event.size().width(), event.size().height())
            window.resize(size, size)
            if cards: update_icon_size(cards)
        except Exception as e:
            print(f"Ошибка при изменении размера окна: {e}")
            event.ignore()

        if original_resize: original_resize(event)

    window.resizeEvent = square_resize


def update_icon_size(cards: list, percent=0.8):
    """Обновляет размер иконок на кнопках в зависимости от их текущего размера.

    Args:
        cards: Список кнопок (QPushButton), у которых нужно обновить размер иконок.
        percent: процент размера иконок относительно кнопки (по умолчанию 80%).

    Raises:
        TypeError: Если cards не является списком.
        TypeError: Если элементы cards не являются QPushButton.
    """
    if not isinstance(cards, list):
        raise TypeError(f"cards должен быть списком, получен {type(cards)}")

    for card in cards:
        if not isinstance(card, QPushButton):
            raise TypeError("Все элементы cards должны быть QPushButton.")
        try:
            img_size = QSize(int(card.size().width() * percent),
                             int(card.size().height() *percent))
            card.setIconSize(img_size)
        except Exception as e:
            print(f"Ошибка при обновлении иконки кнопки: {e}")
            continue