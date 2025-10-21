import os

USERS_FILE = "users.txt"

def check_user(user_id: int, path: str = USERS_FILE) -> bool:
    """
    Проверяет, встречался ли user_id ранее.
    Возвращает True, если уже был, иначе False.
    """
    user_id = str(user_id)
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() == user_id:
                return True
    return False


def add_user(user_id: int, path: str = USERS_FILE) -> None:
    """
    Добавляет user_id в файл, если его там ещё нет.
    """
    if not check_user(user_id, path):
        with open(path, "a", encoding="utf-8") as f:
            f.write(str(user_id) + "\n")
