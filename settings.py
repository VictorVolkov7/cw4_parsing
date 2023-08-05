# Пути до файлов с данными
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent
HH_VACANCIES_ROOT = ROOT_PATH.joinpath('data', 'hh_vacancies.json')
SJ_VACANCIES_ROOT = ROOT_PATH.joinpath('data', 'sj_vacancies.json')
GENERAL_VACANCIES_ROOT = ROOT_PATH.joinpath('data', 'general_vacancies.json')
