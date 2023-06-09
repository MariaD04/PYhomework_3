import json
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup

HOST = 'https://spb.hh.ru'
MAIN = f'{HOST}/search/vacancy?text=python&area=1&area=2'

def get_headers():
    return Headers(browser='Google', os='win').generate()

links_list_ = []
list_ = []
links_list = []
salary_list = []
city_list = []
company_list = []
parsed_data = []

main_page = requests.get(MAIN, headers=get_headers()).text

bs = BeautifulSoup(main_page, features='lxml')
vacancy_list = bs.find_all('a', class_='serp-item__title')
for vacancy in vacancy_list:
    link = vacancy['href']
    links_list_.append(link)
    vacancy_link = requests.get(link,headers=get_headers()).text
    bs_vacancy = BeautifulSoup(vacancy_link, features='lxml')
    description = bs_vacancy.find('div', {'data-qa': 'vacancy-description'}).text
    if not description:
        continue
    if ('Django' or 'Flask' or 'django' or'flask') in description:
        list_.append('+')
    else:
        list_.append('-')
for link, symbol in zip(links_list_, list_):
    if symbol == '+':
        links_list.append(link)

for link in links_list:
    salary_link = requests.get(link,headers=get_headers()).text
    bs_salary = BeautifulSoup(salary_link, features='lxml')
    salary = bs_salary.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text
    salary_list.append(salary)

for link in links_list:
    company_parsed = requests.get(link,headers=get_headers()).text
    bs_company_ = BeautifulSoup(company_parsed, features='lxml')
    company_link_ = bs_company_.find('a', class_='bloko-link_kind-tertiary')['href']
    company_href = f'{HOST}{company_link_}'
    company_link = requests.get(company_href,headers=get_headers()).text
    bs_company = BeautifulSoup(company_link, features='lxml')
    company = bs_company.find('span', class_='company-header-title-name').text
    company_list.append(company)

for link in links_list:
    city_link = requests.get(link, headers=get_headers()).text 
    bs_city = BeautifulSoup(city_link, features='lxml')
    city = bs_city.find('p', {'data-qa': 'vacancy-view-location'})
    if not city:
        city = bs_city.find('span', {'data-qa': 'vacancy-view-raw-address'})
        if not city:
            continue
    city_text = city.text
    city_list.append(city_text)

all_data = zip(links_list, salary_list, company_list, city_list)
for link, salary, company, city in all_data:
    parsed_data_dict = {
        'link': link,
        'salary': salary,
        'company': company,
        'city': city
    }
    parsed_data.append(parsed_data_dict)

with open('parsed_data.json', 'w', encoding='utf-8') as data:
    json.dump(parsed_data, data, indent=2, ensure_ascii=False)
    

