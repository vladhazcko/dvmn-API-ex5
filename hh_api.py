import requests
from pprint import pprint
from itertools import count
from scripts import predict_rub_salary

HOST = 'https://api.hh.ru/'
PROGRAMMING_LANGUAGES = (
    'Python', 'Java', 'Javascript',
    'Ruby', 'PHP', 'C++',
    'C#', 'GO', 'Shell',
    'Scala', 'C', '1С'
)


def get_hh_statistics(programming_languages=PROGRAMMING_LANGUAGES):
    vacancies_stats = {}

    for programming_language in programming_languages:
        vacancies = get_hh_vacancies(text=programming_language)

        list_salary = []

        for vacancy in vacancies:
            predicted_salary = predict_rub_salary_for_hh(vacancy)
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


def get_hh_vacancies(get_all=False, **kwargs):
    vacancies_list = []

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

        vacancies_list += response.json()['items']
        pages_found = int(response.json()['pages']) - 1
        if page >= pages_found:
            return vacancies_list


def predict_rub_salary_for_hh(vacancy):
    salary = vacancy.get('salary', None)
    if not salary or salary.get('currency') != 'RUR':
        return None
    salary_from = salary.get('from', None)
    salary_to = salary.get('to', None)
    return predict_rub_salary(salary_from, salary_to)
