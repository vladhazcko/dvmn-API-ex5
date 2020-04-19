import requests
from pprint import pprint

HOST = 'https://api.hh.ru/'


def main():
    programming_languages = (
        'Python', 'Java', 'Javascript',
        'Ruby', 'PHP', 'C++',
        'C#', 'GO', 'Shell',
        'Scala', 'C'
    )

    # vacansies_stats = {}
    # for programming_language in programming_languages:
    #     count = get_hh_vacancies(text=programming_language).json()['found']
    #     vacansies_stats[programming_language] = count
    #
    # for row in sorted(vacansies_stats.items(), key=lambda item: item[1], reverse=True):
    #     print(row)

    # python_salary_stats = []
    # response = get_hh_vacancies()
    # for job in response.json()['items']:
    #     if job['salary'] is None:
    #         continue
    #
    #     salary = {}
    #     for parameter, value in job['salary'].items():
    #         salary[parameter] = value
    #     python_salary_stats.append(salary)
    #
    # pprint(python_salary_stats)

    response = get_hh_vacancies()
    for job in response.json()['items']:
        print(predict_rub_salary(job))


def get_hh_vacancies(**kwargs) -> requests:
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

    response = requests.get(request_url, params)
    response.raise_for_status()
    return response


def predict_rub_salary(job):
    salary = job['salary']
    if salary is None or salary['currency'] != 'RUR':
        return None

    if salary['from'] is None and salary['to'] is None:
        return None
    if salary['from'] is None:
        return salary['to'] * 0.8
    if salary['to'] is None:
        return salary['from'] * 1.2
    return (salary['to'] + salary['from']) // 2


if __name__ == '__main__':
    main()
