import requests
from scripts import predict_rub_salary
from itertools import count

HOST = 'https://api.superjob.ru/'
API_VERSION = '2.30'


def get_superjob_statistics(secret_key, programming_languages):
    vacancies_stats = {}

    for programming_language in programming_languages:
        vacancies = get_superjob_vacancies(
            secret_key,
            keyword=f'Программист {programming_language}',
            town=4
        )

        prog_lang_salaries = []

        for vacancy in vacancies:
            predicted_salary = predict_rub_salary_for_superjob(vacancy)
            if predicted_salary:
                prog_lang_salaries.append(predicted_salary)

        vacancies_stats[programming_language] = {
            'vacancies_found': len(vacancies),
            'vacancies_processed': len(prog_lang_salaries),
            'average_salary':
                sum(prog_lang_salaries) // len(prog_lang_salaries) if len(prog_lang_salaries)
                else None
        }

    return vacancies_stats


def get_superjob_vacancies(secret_key, **kwargs):
    vacancies = []

    method = '/vacancies/'
    request_url = HOST + API_VERSION + method
    headers = {'X-Api-App-Id': secret_key}
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
        response.raise_for_status()

        response_decode = response.json()
        vacancies += response_decode['objects']
        if not response_decode['more']:
            return vacancies


def predict_rub_salary_for_superjob(vacancy):
    if not vacancy or vacancy.get('currency') != 'rub':
        return None
    salary_from = vacancy.get('payment_from', None)
    salary_to = vacancy.get('payment_to', None)
    return predict_rub_salary(salary_from, salary_to)
