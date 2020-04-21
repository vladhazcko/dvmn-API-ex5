import requests
from scripts import predict_rub_salary
from itertools import count

HOST = 'https://api.hh.ru/'


def get_hh_statistics(programming_languages):
    vacancies_stats = {}

    for programming_language in programming_languages:
        vacancies = get_hh_vacancies(text=programming_language)

        prog_lang_salaries = []

        for vacancy in vacancies:
            predicted_salary = predict_rub_salary_for_hh(vacancy)
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


def get_hh_vacancies(get_all=False, **kwargs):
    vacancies = []

    method = 'vacancies'
    request_url = HOST + method
    params = {
        'specialization': kwargs.get('specialization', ('1.221',)),
        'page': kwargs.get('page', 0),
        'per_page': kwargs.get('per_page', 20),
        'period': kwargs.get('period', 30),
        'text': kwargs.get('text', ''),
    }
    for param in ('search_field', 'area'):
        if param in kwargs:
            params[param] = kwargs[param]

    for page in count(0):
        params['page'] = page
        response = requests.get(request_url, params)
        response.raise_for_status()

        response_decode = response.json()
        vacancies += response_decode['items']
        pages_found = int(response_decode['pages']) - 1
        if page >= pages_found:
            return vacancies


def predict_rub_salary_for_hh(vacancy):
    salary = vacancy.get('salary', None)
    if not salary or salary.get('currency') != 'RUR':
        return None
    salary_from = salary.get('from', None)
    salary_to = salary.get('to', None)
    return predict_rub_salary(salary_from, salary_to)
