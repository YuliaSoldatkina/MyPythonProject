# my-project/src/my_project/decorators.py

"""Модуль для декораторов, включая декоратор log."""

def log(func):
    """Заглушка для декоратора log. Реализуем позже."""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
