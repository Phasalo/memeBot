from os import listdir, unlink
from os.path import join, isfile, islink, isdir, dirname, abspath
from typing import Optional


def clear(temp_dir: Optional[str] = None) -> bool:
    if not temp_dir:
        temp_dir = dirname(__file__)

    try:
        for filename in listdir(temp_dir):
            file_path = join(temp_dir, filename)

            if abspath(file_path) == abspath(__file__):
                continue

            if isfile(file_path) or islink(file_path):
                unlink(file_path)
            elif isdir(file_path):
                clear(file_path)
        return True
    except Exception as e:
        print(f'Ошибка при удалении: {e}')
        return False
