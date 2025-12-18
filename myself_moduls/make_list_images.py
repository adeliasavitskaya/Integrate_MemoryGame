import os
from random import sample, shuffle


def list_files(dir_paths):
    """Находит изображения в указанных директориях и
    подготавливает пары для игры.

    Требуется минимум 8 уникальных изображений для создания 8 пар карточек.

    Args:
        dir_paths (tuple): Кортеж путей к директориям для поиска изображений.

    Returns:
        List[str]: Список из 16 путей к изображениям (8 уникальных × 2).

    Raises:
        FileNotFoundError: Если не найдено минимум 8 изображений.
    """
    all_images = []
    for dir_path in dir_paths:
        if not os.path.isdir(dir_path):
            continue
        try:
            for file in os.scandir(dir_path):
                if file.is_file() and file.name.lower().endswith(
                    (".png", ".jpg", ".jpeg")
                ):
                    all_images.append(file.path)
        except Exception as e:
            print(f"Нет доступа к директории {dir_path}: {e}")
            continue
    if len(all_images) < 8:
        raise FileNotFoundError(
            f"Недостаточно изображений для игры в: {dir_paths}"
        )
    selected = sample(all_images, 8)
    pairs = selected * 2
    shuffle(pairs)
    return pairs
