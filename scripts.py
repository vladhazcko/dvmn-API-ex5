from terminaltables import SingleTable


def predict_rub_salary(salary_from, salary_to):
    if not salary_from and not salary_to:
        return None
    elif not salary_from:
        return round(salary_to * 0.8)
    elif not salary_to:
        return round(salary_from * 1.2)
    else:
        return (salary_to + salary_from) // 2


def get_table_vacancies(vacancy_stats, title):
    table_data = [
        ('Язык программирования',
         'Вакансий найдено',
         'Вакансий обработано',
         'Средняя зарплата')
    ]
    for programming_language, stats in vacancy_stats.items():
        table_data.append(
            (programming_language,
             stats['vacancies_found'],
             stats['vacancies_processed'],
             stats['average_salary']
             )
        )
    table_instance = SingleTable(table_data, title)
    return table_instance
