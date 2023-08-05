import json
from abc import ABC, abstractmethod


class Saver(ABC):
    """
    Абстрактный класс для работы с файлами.
    """
    @abstractmethod
    def save_into(self, path, data):
        pass


class JSONSaver(Saver):
    """
    Класс для работы с файлами .json.
    """
    def save_into(self, path, data: list[dict]):
        """
        Сохранение вакансий в json. Принимает путь и данные.
        :param path: Путь.
        :param data: Данные.:
        """
        with open(path, 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

