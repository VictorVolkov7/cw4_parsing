from src.saver import JSONSaver
from src.utils import choice_platform, choice_saver, choice_filter, repeated_request
from src.vacancy import Vacancy


def main():
    continue_search = True
    continue_filter = True
    try:
        # Блок для выбора платформ и расширения для сохранения
        while continue_search:
            # Выбор платформы пользователем и ключевого слова для поиска вакансий
            vacancies, user_choice_platform = choice_platform()

            # Получает выбранное расширение и путь до файла
            saver_choice, user_choice_saver = choice_saver(user_choice_platform)
            # Если пользователь выбрал расширение json
            if user_choice_saver == 1:
                json_saver = JSONSaver()
                json_saver.save_into(saver_choice, vacancies)

                vacancy = Vacancy()
                vacancy.instantiate_from_json(saver_choice)

                print(f'Найдено {len(vacancy.all_vacancies)} вакансий. Приступим к работе!.')

                # Блок для работы с вакансиями по фильтрам
                while continue_filter:
                    while True:
                        try:
                            choice_filter()
                        except TypeError:
                            break

                    if not repeated_request('Хотите выбрать другие фильтры? (да/нет): '):
                        continue_filter = False

            if not repeated_request('Хотите выбрать другую ключевое слово для поиска вакансий? (да/нет): '):
                print('Всего доброго, увидимся позже!\n')
                continue_search = False
    except TypeError:
        print('Всего доброго, увидимся позже!\n')


if __name__ == '__main__':
    main()
