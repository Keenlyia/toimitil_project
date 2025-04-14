from load_django import *
from parser_app.models import *
import json
import os

export_data = []

# Перебір всіх компаній в json_field
for item in Company.objects.filter(json_field__isnull=False):  # Обираємо компанії з даними в json_field

    print()
    print('#' * 50)

    # Перевірка типу даних в json_field
    if isinstance(item.json_field, str):
        company_data = json.loads(item.json_field)
    else:
        company_data = item.json_field

    # Витягування основних даних компанії
    company_name = company_data.get('name', None)
    print('Company Name: ', company_name)

    company_url = company_data.get('url', None)
    print('Company URL: ', company_url)

    logo_url = company_data.get('logo', None)
    print('Company Logo URL: ', logo_url)

    address = company_data.get('address', None)
    print('Company Address: ', address)

    city = company_data.get('city', None)
    print('City: ', city)

    zip_code = company_data.get('zip_code', None)
    print('Zip Code: ', zip_code)

    parent_name = company_data.get('parent_name', None)
    print('Parent Company Name: ', parent_name)

    parent_logo_url = company_data.get('parent_logo', None)
    print('Parent Company Logo URL: ', parent_logo_url)

    parent_id = company_data.get('parent_id', None)
    print('Parent Company ID: ', parent_id)

    ad_guarantee = company_data.get('adGuarantee', False)
    print('Ad Guarantee: ', ad_guarantee)

    # Оновлення об'єкту в БД
    item.name = company_name
    item.url = company_url
    item.logo_url = logo_url
    item.address = address
    item.city = city
    item.zip_code = zip_code
    item.parent_name = parent_name
    item.parent_logo_url = parent_logo_url
    item.parent_id = parent_id
    item.ad_guarantee = ad_guarantee
    item.save()

    # Додаємо до експорту
    export_data.append({
        "name": company_name,
        "url": company_url,
        "logo_url": logo_url,
        "address": address,
        "city": city,
        "zip_code": zip_code,
        "parent_name": parent_name,
        "parent_logo_url": parent_logo_url,
        "parent_id": parent_id,
        "ad_guarantee": ad_guarantee
    })

# Збереження у json
with open('../results/companies_data.json', 'w',
          encoding='utf-8') as file:
    json.dump(export_data, file,
              ensure_ascii=False, indent=4)

print("Дані компаній збережено у файл: results/companies_data.json")
