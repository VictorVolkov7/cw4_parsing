from settings import HH_VACANCIES_ROOT, SJ_VACANCIES_ROOT, GENERAL_VACANCIES_ROOT
from src.platforms_API import HeadHuntersAPI, SuperJobAPI
from src.vacancy import Vacancy

vacancy = Vacancy()


def choice_platform():
    """
    Функция спрашивает у пользователя с какой платформой будем работать.
    :return: Возвращает список словарей с вакансиями.
    """
    while True:
        try:
            user_input: int = int(input('\nВыберите платформу для поиска вакансий цифрами, от 1 до 4\n'
                                        '1 - HeadHunters\n'
                                        '2 - SuperJob\n'
                                        '3 - Везде\n'
                                        '4 - Не хочу искать вакансии\n'))
            if user_input == 1:
                user_vacancy_keyword: str = input('Введите ключевые слова для поиска вакансий: ').lower()
                print('Получаем список вакансий с вашим ключевым словом с платформы HeadHunters, ожидайте...\n')
                hh_connection = HeadHuntersAPI(user_vacancy_keyword)
                hh_vacancies = hh_connection.get_shorts_info()
                return hh_vacancies, user_input
            elif user_input == 2:
                user_vacancy_keyword: str = input('Введите ключевые слова для поиска вакансий: ').lower()
                print('Получаем список вакансий с вашим ключевым словом с платформы SuperJob, ожидайте...\n')
                sj_connection = SuperJobAPI(user_vacancy_keyword)
                sj_vacancies = sj_connection.get_shorts_info()
                return sj_vacancies, user_input
            elif user_input == 3:
                user_vacancy_keyword: str = input('Введите ключевые слова для поиска вакансий: ').lower()
                print('Получаем список вакансий с вашим ключевым словом с обоих платформ, ожидайте...\n')
                hh_connection = HeadHuntersAPI(user_vacancy_keyword)
                sj_connection = SuperJobAPI(user_vacancy_keyword)
                general_vacancies = hh_connection + sj_connection
                return general_vacancies, user_input
            elif user_input == 4:
                break
            else:
                print('Не понял вас, введите еще раз!\n')
        except ValueError:
            print('Значение должно быть целым числом от 1 до 4\n')


def choice_saver(user_choice: int) -> int | object:
    """
    Функция, которая принимает выбор пользователя по платформе и возвращает путь, до файла с выбранной платформой.
    :param user_choice: Выбор пользователя по платформе.
    :return: Путь, до файла с выбранной платформой и выбранное расширение
    """
    while True:
        try:
            user_input: int = int(input('Выберите расширение для сохранения вакансий, цифрами от 1 до -\n'
                                        '1 - JSON\n'))  # '2 - Exel\n'# '3 - CSV\n'
            if user_input == 1:
                if user_choice == 1:
                    print('Идет сохранение в json файл, ожидайте...\n')
                    return HH_VACANCIES_ROOT, user_input
                elif user_choice == 2:
                    print('Идет сохранение в json файл, ожидайте...\n')
                    return SJ_VACANCIES_ROOT, user_input
                elif user_choice == 3:
                    print('Идет сохранение в json файл, ожидайте...\n')
                    return GENERAL_VACANCIES_ROOT, user_input
            else:
                print('Не понял вас, введите еще раз!\n')
        except ValueError:
            print('Значение должно быть целым числом от 1 до 3\n')


def choice_filter() -> None:
    """
    Функция, для выбора фильтров поиска.
    :return: Возвращает None, если пользователь не хочет работать
    """
    filter_options = {
        1: city_count_filter,
        2: salary_top_filter,
        3: keyword_filter,
        4: all_vacancy,
        5: 'Не хочу работать с вакансиями.'
    }

    while True:
        try:
            user_input: int = int(input('Выберите фильтры для вывода вакансий, цифрами от 1 до 4\n'
                                        '1 - Поиск N вакансий по городам\n'
                                        '2 - Вывести топ N вакансий по средней зарплате \n'
                                        '3 - Вывести вакансии содержащие в описании ключевые слова\n'
                                        '4 - Вывести все вакансии\n'
                                        '5 - Не хочу работать с вакансиями / выбрать другое ключевое слово.\n'))

            filter_options.get(user_input, lambda: print("Неверный выбор"))()

            if user_input == 5:
                return None

        except ValueError:
            print("Пожалуйста, введите число от 1 до 5.")


def city_count_filter():
    """
    Фильтр для поиска по городам. Пользователь вводит город, происходит проверка,
    и дальше этот город передается в метод класса Vacancy для сортировки по городам и возвращает список
    Этот список передается в функцию page_filter для вывода вакансий по странично
    """
    while True:
        user_city: str = input('Введите город для поиска: ')
        if user_city.isdigit():
            print('Введите корректное название города.')
        elif len(user_city) > 20:
            print('Название города не должно превышать 20 символов')
        else:
            break

    filter_city = vacancy.vacancies_for_city(user_city)
    print(f'Найдено {len(filter_city)} вакансий в городе {user_city}')

    user_count = get_check_number(filter_city, 'Введите целое число, указывающее сколько вакансий будет на '
                                               'странице (оптимально 50), не превышающее количество найденных вакансий:'
                                  )
    page_filter(filter_city, user_count)


def salary_top_filter():
    """
    Фильтр для вывода топ вакансий. Пользователь вводит количество вакансий, список вакансий сортируется
    с помощью метода класса Vacancy и с помощью среза ему это количество выводится
    и спрашивается у пользователя удалять найденные вакансии или нет.
    """
    while True:
        user_count = get_check_number(vacancy.all_vacancies, 'Введите количество вакансий, для вашего топа: ')

        vacancy.vacancies_for_salary()
        for vac in vacancy.all_vacancies[0: user_count]:
            print(vac)

        if repeated_request('Хотите удалить отображенные вакансии? (да/нет): '):
            vacancy.all_vacancies = vacancy.all_vacancies[user_count:]

        if not repeated_request('Хотите сделать еще один запрос? (да/нет): '):
            break


def keyword_filter():
    """
    Фильтр для поиска по ключевому слову в описании. Пользователь вводит ключевое слово,
    и дальше это ключевое слово передается в метод класса Vacancy для сортировки по ключевому слову и возвращает список
    Этот список через итерацию печатается пользователю
    и спрашивается у пользователя удалять найденные вакансии или нет
    """
    while True:
        user_keyword: str = input('Введите одно, два ключевых слова для поиска в описании вакансии: ')
        filter_keyword = vacancy.vacancies_for_keyword(user_keyword)
        print(f'Найдено {len(filter_keyword)} вакансий с ключевым словом {user_keyword}')

        all_vacancies_to_delete = []

        for vac in filter_keyword:
            print(vac)
            all_vacancies_to_delete.append(vac)

        if len(filter_keyword) == 0:
            pass
        else:
            if repeated_request('Хотите удалить отображенные вакансии? (да/нет): '):
                for vac_1 in all_vacancies_to_delete:
                    vacancy.all_vacancies.remove(vac_1)

        if not repeated_request('Хотите повторить запрос или сменить кодовое слово? (да/нет): '):
            break


def all_vacancy():
    """
    Выводит постранично пользователю все найденные вакансии с его ключевым словом.
    :return:
    """
    all_vac: list = vacancy.all_vacancies
    user_count = get_check_number(all_vac, 'Введите целое число, указывающее сколько вакансий будет на '
                                           'странице (оптимально 50), не превышающее количество найденных вакансий: ')
    page_filter(all_vac, user_count)


def page_filter(list_: list, user_count: int):
    """
    Фильтр, который принимает список и пользовательское число и частями выдает вакансии,
    чтобы вывести следующие, следует нажать пробел
    :param list_: Список для итерации
    :param user_count: Пользовательское число (сколько вакансий на одной странице)
    :return:
    """
    for num in range(0, len(list_), user_count):
        slice_: list = list_[num: num + user_count]
        print("\n".join(map(str, slice_)))

        if (num + user_count) < len(list_):
            input("Нажмите Enter для продолжения...")
        elif user_count > len(list_):
            print('Введите корректное число.')


def get_check_number(list_: list, massage: str) -> int:
    """
    Функция для проверки числа в допустимом диапазоне и чтобы оно было целое,
    используется для функции page_filter
    :param list_: Список
    :param massage: Сообщение для пользователя
    :return: Действительное число
    """
    while True:
        user_count = input(f'{massage}')
        if user_count.isdigit():
            user_count = int(user_count)
            if 0 < user_count <= len(list_):
                return user_count
            else:
                print("Введите число в пределах допустимого диапазона.")
        else:
            print("Пожалуйста, введите целое число.")


def repeated_request(massage: str) -> bool:
    """
    Функция, которая принимает какое-то сообщение и служит для повторной реализации какого то кода,
    возвращает boll и брейкует циклы while True
    :param massage:
    :return: bool
    """
    while True:
        user_input: str = input(massage).lower()
        if user_input == 'нет':
            return False
        elif user_input == 'да':
            return True
        else:
            print('Не понял вас, повторите ещё.')
