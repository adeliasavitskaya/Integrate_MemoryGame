import os

_cache = {}
_project_root = None
def find_project_root(marker='README.md'):
    """Находит корневую директорию проекта по указанному маркеру.

    Ищет файл-маркер, перемещаясь вверх по иерархии директорий.

    Args:
        marker (str): Имя файла или директории, служащей маркером корня.
        По умолчанию 'README.md'.

    Returns:
        str: Абсолютный путь к директории, содержащей маркер.

    Raises:
        FileNotFoundError: Если маркер не найден.
    """
    global _project_root
    if _project_root:
        return _project_root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.exists(os.path.join(current_dir, marker)):
            _project_root = current_dir
            return _project_root
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break

        current_dir = parent_dir

    raise FileNotFoundError(f"Не найден маркер '{marker}'")

def get_path(name):
    """
    Находит путь к файлу или папке в проекте.

    Алгоритм поиска:
    1. Проверяем кеш (_cache)
    2. Ищет от корня программы

    Args:
        name (str): Имя файла или папки для поиска.

    Returns:
        str: Полный абсолютный путь к файлу или папке.

    Raises:
        ValueError: Если имя не указано.
        FileExistsError: Если объект с таким именем найден в нескольких местах.
        FileNotFoundError: Если объект не найден в проекте.
    """
    if not name:
        raise ValueError("Имя не указано")

    if name in _cache:
        return _cache[name]

    base_dir = find_project_root()
    found = None
    for root, dirs, files in os.walk(base_dir):
        if any(ignore in root for ignore in ['.git', '.venv', '__pycache__']):
            continue

        if name in dirs or name in files:
            path = os.path.join(root, name)
            if found is None:
                found = path
            else:
                raise FileExistsError(f"'{name}' найден в нескольких местах")

    if found is None:
        raise FileNotFoundError(f"Не найден: {name}")

    _cache[name] = found
    return found