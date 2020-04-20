import requests
from dotenv import load_dotenv
import os
from scripts import predict_rub_salary, get_table_vacancies
from itertools import count
from terminaltables import SingleTable

load_dotenv()
SECRET_KEY = os.getenv('SUPERJOB_SECRET_KEY')
HOST = 'https://api.superjob.ru/'
API_VERSION = '2.30'
PROGRAMMING_LANGUAGES = (
        'Python', 'Java', 'Javascript',
        'Ruby', 'PHP', 'C++',
        'C#', 'GO', 'Shell',
        'Scala', 'C', '1С'
)


def get_superjob_statistics(programming_languages=PROGRAMMING_LANGUAGES):
    vacancies_stats = {}

    for programming_language in programming_languages:
        vacancies = get_superjob_vacancies(
            keyword=f'Программист {programming_language}',
            town=4
        )

        list_salary = []

        for vacancy in vacancies:
            predicted_salary = predict_rub_salary_for_superjob(vacancy)
            if predicted_salary:
                list_salary.append(predicted_salary)

        vacancies_stats[programming_language] = {}
        vacancies_stats[programming_language]['vacancies_found'] = len(vacancies)
        vacancies_stats[programming_language]['vacancies_processed'] = len(list_salary)
        if len(list_salary):
            vacancies_stats[programming_language]['average_salary'] = sum(list_salary) // len(list_salary)
        else:
            vacancies_stats[programming_language]['average_salary'] = None

    return vacancies_stats


def get_superjob_vacancies(**kwargs):
    vacancies_list = []

    method = '/vacancies/'
    request_url = HOST + API_VERSION + method
    headers = {'X-Api-App-Id': SECRET_KEY}
    params = {
        'page': kwargs.get('page', 0),
        'period': kwargs.get('period', 0),
        'count': kwargs.get('count', 20),
    }
    for param in ('keyword', 'town'):
        if param in kwargs:
            params[param] = kwargs[param]

    for page in count(0):
        params['page'] = page
        response = requests.get(request_url, params, headers=headers)
        vacancies_list += response.json()['objects']
        if not response.json()['more']:
            return vacancies_list


def predict_rub_salary_for_superjob(vacancy):
    if not vacancy or vacancy.get('currency') != 'rub':
        return None
    salary_from = vacancy.get('payment_from', None)
    salary_to = vacancy.get('payment_to', None)
    return predict_rub_salary(salary_from, salary_to)
