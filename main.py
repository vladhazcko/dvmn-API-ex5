from scripts import get_table_vacancies
from superjob_api import get_superjob_statistics
from hh_api import get_hh_statistics

PROGRAMMING_LANGUAGES = (
    'Python', 'Java', 'Javascript',
    'Ruby', 'PHP', 'C++',
    'C#', 'GO', 'Shell',
    'Scala', 'C', '1С'
)


def main():
    vacancies_stats_hh = get_hh_statistics(PROGRAMMING_LANGUAGES)
    vacancies_stats_superjob = get_superjob_statistics(PROGRAMMING_LANGUAGES)

    table_hh = get_table_vacancies(vacancies_stats_hh, 'HeadHunter Moscow')
    print(table_hh.table)

    table_superjob = get_table_vacancies(vacancies_stats_superjob, 'SuperJob Moscow')
    print(table_superjob.table)


if __name__ == '__main__':
    main()
