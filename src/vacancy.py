import json


class Vacancy:
    all_vacancies = []

    def __init__(self, name=None, place=None, url=None, salary_from=None, salary_to=None, currency=None, title=None):
        """
        Инициализация класса Vacancy.

        :param name: Название вакансии.
        :param place: Город.
        :param url: Ссылка на вакансию.
        :param salary_from: Минимальная зарплата.
        :param salary_to: Предельная зарплата.
        :param currency: Валюта.
        :param title: Описание вакансии.
        """
        self.name: str = name
        self.place: str = place
        self.url: str = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency: str = currency
        self.title: str = title

        Vacancy.all_vacancies.append(self)

    def __str__(self):
        """
        Возвращает информацию для пользователей.
        """
        self.title = self.title.replace('\n', '')
        return (f'\nВакансия: {self.name}, в городе {self.place}.\n'
                f'Зарплата: от "{self.salary_from}" до "{self.salary_to}" {self.currency}\n'
                f'Описание:\n{self.title}\n'
                f'Ссылка: {self.url}')

    def __gt__(self, other):
        """
        Сравнивает среднее значение зарплаты между вакансиями
        """
        if issubclass(other.__class__, self.__class__):
            return self.calculate_salary() > other.calculate_salary()

    def calculate_salary(self) -> object:
        """
        Принимает минимальную и предельную зарплату, переводит по курсу валют
        """
        salary_from, salary_to = self.salary_from, self.salary_to
        if salary_from == 'Минимальная зарплата не указана':
            salary_from: int = 0
        if salary_to == 'Предельная зарплата не указана':
            salary_to: int = 0

        if self.currency in ['USD', 'usd']:
            factor: int = 92
        elif self.currency in ['BYR', 'byr']:
            factor: int = 37
        elif self.currency in ['KZT', 'kzt']:
            factor: float = 0.21
        elif self.currency in ['EUR', 'eur']:
            factor: int = 105
        elif self.currency in ['UZS', 'uzs']:
            factor: float = 0.008
        else:
            factor: int = 1

        salary_from *= factor
        salary_to *= factor

        return (salary_from + salary_to) / 2

    @classmethod
    def instantiate_from_json(cls, path):
        """
        Инициализирует экземпляры класса Vacancy данными из файла data/...
        """
        cls.all_vacancies: list = []

        if not path.exists():
            raise FileNotFoundError('Отсутствует файл')

        with open(path, encoding='utf-8') as f:
            vacancies = json.load(f)

            for vac in vacancies:
                vac: dict
                cls(**vac)

    @classmethod
    def vacancies_for_city(cls, city) -> list:
        """
        Сортирует вакансии по городу и возвращает список вакансий с нужным городом.
        """
        filter_city: list = []
        for vac in cls.all_vacancies:
            if vac.place == city:
                filter_city.append(vac)
        return filter_city

    @classmethod
    def vacancies_for_salary(cls):
        """
        Сортирует вакансии по зарплате и возвращает отфильтрованный список экземпляров класса по убиванию зарплаты.
        """
        cls.all_vacancies.sort(reverse=True)

    @classmethod
    def vacancies_for_keyword(cls, keyword) -> list:
        """
        Сортирует вакансии по ключевому слову и возвращает список вакансий с нужным ключевым словом в описании.
        """
        filter_keyword: list = []
        for vac in cls.all_vacancies:
            if keyword in vac.title:
                filter_keyword.append(vac)
        return filter_keyword
