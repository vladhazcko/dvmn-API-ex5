import requests
from pprint import pprint
from itertools import count

HOST = 'https://api.hh.ru/'


def main():
    programming_languages = (
        'Python', 'Java', 'Javascript',
        'Ruby', 'PHP', 'C++',
        'C#', 'GO', 'Shell',
        'Scala', 'C'
    )

    vacancies_stats = {}

    for programming_language in programming_languages:
        response = get_hh_vacancies(text=programming_language)

        list_salary = []

        for job in response:
            predicted_salary = predict_rub_salary(job)
            if predicted_salary is not None:
                list_salary.append(predicted_salary)

        vacancies_stats[programming_language] = {}
        vacancies_stats[programming_language]['vacancies_found'] = len(response)
        vacancies_stats[programming_language]['vacancies_processed'] = len(list_salary)
        vacancies_stats[programming_language]['average_salary'] = sum(list_salary) // len(list_salary)

    pprint(vacancies_stats)


def get_hh_vacancies(get_all=False, **kwargs) -> requests:
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
        response = requests.get(request_url, params)
        response.raise_for_status()

        vacancies_list += response.json()['items']
        pages_found = int(response.json()['pages'])
        if page >= pages_found:
            return vacancies_list


def predict_rub_salary(job):
    salary = job['salary']
    if salary is None or salary['currency'] != 'RUR':
        return None
    if salary['from'] is None and salary['to'] is None:
        return None
    if salary['from'] is None:
        return round(salary['to'] * 0.8)
    if salary['to'] is None:
        return round(salary['from'] * 1.2)
    return (salary['to'] + salary['from']) // 2


if __name__ == '__main__':
    main()
