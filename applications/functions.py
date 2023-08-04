from bs4 import BeautifulSoup
import requests
from time import sleep
import fake_headers
import random


# hh.ru видимо сильно защищены от спама с одного браузера - написал эту функцию которая каждый раз с рандомного браузера стучится
# и с рандомной os стучиться
def generate_fake_headers():
    fake_browser_list = ['firefox', 'edge', 'chrome', 'yabrowser', 'safari', 'opera', 'firefox2', 'edge2', 'operagx']
    fake_os_list = ['win', 'linux', 'macos']
    fake_browser = random.choice(fake_browser_list)
    fake_os = random.choice(fake_os_list)

    return fake_headers.Headers(browser=fake_browser, os=fake_os)


def find_vacancy():
    data = []

    headers_gen = generate_fake_headers()
    sleep(3)
    response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',
                            headers=headers_gen.generate())
    html_data = response.text
    hh_main = BeautifulSoup(html_data, features='lxml')

    vacancy_list_tag = hh_main.find(name='main', class_='vacancy-serp-content')
    vacancy_tags = vacancy_list_tag.find_all(name='div', class_='vacancy-serp-item__layout')

    for vacancy_tag in vacancy_tags:
        header_tag = vacancy_tag.find('h3')
        vacancy_name = header_tag.text

        a_tag = header_tag.find('a')
        link = a_tag['href']

        sleep(1)
        headers_gen = generate_fake_headers()

        vacancy_response = requests.get(link, headers=headers_gen.generate())
        vacancy_html_data = vacancy_response.text

        vacancy_main = BeautifulSoup(vacancy_html_data, features='lxml')
        vacancy_description_tag = vacancy_main.find(name='div', class_='vacancy-description')

        vacancy_salary_tag = vacancy_main.find(name='span', class_='bloko-header-section-2 bloko-header-section-2_lite')
        vacancy_salary = vacancy_salary_tag.text

        vacancy_company_info_tag = vacancy_main.find(name='div',
                                                     class_='vacancy-company-redesigned')
        # условие нужно чтоб вакансии построенные особым образом пропускать
        # например https://spb.hh.ru/vacancy/84439688?from=vacancy_search_list&query=python
        # отличается от обычных вакансий где блок инфо справа
        if vacancy_company_info_tag is None:
            continue
        vacancy_company_tag = vacancy_company_info_tag.find(name='div', class_='vacancy-company-details')
        vacancy_company = vacancy_company_tag.text

        # некоторые местоположения содержите в тэги 'а', а некоторые в тэге 'p'
        vacancy_location_tag_p = vacancy_company_info_tag.find(name='p', class_=None)
        vacancy_location_tag_a = vacancy_company_info_tag.find(name='a',
                                                               class_='bloko-link bloko-link_kind-tertiary bloko-link_disable-visited')

        vacancy_location_tag = vacancy_location_tag_p if vacancy_location_tag_p else vacancy_location_tag_a
        vacancy_location = vacancy_location_tag.text

        if 'Django' in vacancy_description_tag.text and 'Flask' in vacancy_description_tag.text:
            # print(vacancy_name, link, vacancy_salary, vacancy_company, vacancy_location)
            data.append(
                {'name': vacancy_name, 'link': link, 'salary': vacancy_salary, 'company': vacancy_company,
                 'location': vacancy_location}
            )
    return data
