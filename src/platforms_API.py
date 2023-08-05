import os
from abc import ABC, abstractmethod

import requests


class PlatformAPI(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_shorts_info(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class HeadHuntersAPI:
    """
    Класс для работы с API HeadHunters и получения вакансий с данного сайта по ключевому слову.
    """

    def __init__(self, vacancy_keyword):
        """
        Инициализация класса HeadHuntersAPI.

        :param vacancy_keyword: Ключевое слово для поиска вакансий.
        """
        self.vacancy_keyword = vacancy_keyword

    def get_vacancies(self) -> list:
        """
        Метод для получения вакансий с API HeadHunters.
        По умолчанию выбирает 2000 вакансий, если такое количество есть (если нет, завершает итерацию)
        :return: vacancies - список вакансий
        """
        vacancies: list = []
        for page in range(0, 20):
            params: dict = {
                'text': f'Name:{self.vacancy_keyword}',  # Текст фильтра. Должно быть слово переданное пользователем
                'page': page,  # Индекс страницы поиска на HH
                'per_page': 100  # Кол-во вакансий на 1 странице
            }
            vacancies.append(requests.get('https://api.hh.ru/vacancies', params).json()["items"])
            if [] in vacancies:
                vacancies.remove([])
                break
        return vacancies

    def get_shorts_info(self) -> list[dict]:
        """
        Метод для получения упрощенной информации о вакансии.
        :return: vacancies - список словарей с вакансиями
        """
        vacancies: list = []
        for vacancy in self.get_vacancies():
            for vac in vacancy:
                vacancy_info: dict = {
                    'name': vac['name'],
                    'place': 'Город не указана' if vac['area'] is None else vac['area']['name'],
                    'salary_from': 'Минимальная зарплата не указана' if vac['salary'] is None or vac['salary'][
                        'from'] is None else vac['salary']['from'],
                    'salary_to': 'Предельная зарплата не указана' if vac['salary'] is None or vac['salary'][
                        'to'] is None else vac['salary']['to'],
                    'currency': '' if vac['salary'] is None else vac['salary']['currency'],
                    'url': vac['alternate_url'],
                    'title': 'Описания и требования нет' if vac[
                        'snippet'] is None else f"{vac['snippet']['requirement']}"
                                                f"{vac['snippet']['responsibility']}"
                }
                vacancies.append(vacancy_info)
        return vacancies

    def __add__(self, other):
        """
        Метод для сложения экземпляров класса
        """
        return self.get_shorts_info() + other.get_shorts_info()


class SuperJobAPI(PlatformAPI):
    """
    Класс для работы с API HeadHunters и получения вакансий с данного сайта по ключевому слову.
    """
    api_key: str = os.getenv('SJ_API_KEY')

    def __init__(self, vacancy_keyword):
        """
        Инициализация класса SuperJobAPI.

        :param vacancy_keyword: Ключевое слово для поиска вакансий.
        """
        self.vacancy_keyword = vacancy_keyword

    def get_vacancies(self) -> list:
        """
        Метод для получения вакансий с API SuperJob.
        По умолчанию выбирает 500 вакансий, если такое количество есть (если нет, завершает итерацию)
        :return: vacancies - список вакансий
        """
        vacancies: list = []
        for page in range(0, 5):
            params: dict = {
                'keyword': self.vacancy_keyword,  # Текст фильтра. Должно быть слово переданное пользователем
                'page': page,  # Индекс страницы поиска на SJ
                'count': 100  # Кол-во вакансий на 1 странице
            }
            my_auth_data = {'X-Api-App-Id': SuperJobAPI.api_key}
            vacancies.append(
                requests.get('https://api.superjob.ru/2.0/vacancies/', headers=my_auth_data, params=params).json()[
                    'objects'])
            if [] in vacancies:
                vacancies.remove([])
                break
        return vacancies

    def get_shorts_info(self) -> list[dict]:
        """
        Метод для получения упрощенной информации о вакансии.
        :return: vacancies - список словарей с вакансиями
        """
        vacancies: list = []
        for vacancy in self.get_vacancies():
            for vac in vacancy:
                vacancy_info: dict = {
                    'name': vac['profession'],
                    'place': 'Город не указана' if vac['town'] is None else vac['town']['title'],
                    'salary_from': 'Минимальная зарплата не указана' if vac['payment_from'] == 0 else vac[
                        'payment_from'],
                    'salary_to': 'Предельная зарплата не указана' if vac['payment_to'] == 0 else vac['payment_to'],
                    'currency': None if vac['currency'] is None else vac['currency'],
                    'url': vac['link'],
                    'title': 'Описания и требования нет' if vac['candidat'] is None else vac['candidat']
                }
                vacancies.append(vacancy_info)
        return vacancies

    def __add__(self, other):
        """
        Метод для сложения экземпляров класса
        """
        return self.get_shorts_info() + other.get_shorts_info()
