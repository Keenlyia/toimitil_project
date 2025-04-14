from load_django import *
from parser_app.models import *

import requests
import json


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "uk,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "ota-cuid": "ff7750ec77febf4b2a9f40e59c926b43aac43ebb",
    "ota-loaded": "1744613061",
    "ota-token": "5f886973f263de925e53116d24be98bbc24182a7a3c64f712e707732eb876879",
    "priority": "u=1, i",
    "referer": "https://toimitilat.oikotie.fi/yritys?page=1",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "",
    "sec-ch-ua-platform": "Windows",
    "sec-ch-ua-platform-version": "10.0.0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

cookies = {
    "PHPSESSID": "c90789ec6ba89c2693eb30ea89f7a181",
    "user_id": "ff7750ec77febf4b2a9f40e59c926b43aac43ebb",
    "_sp_su": "false",
    "consentUUID": "706d58f2-35bb-4389-be89-558ea18cacd5_42",
    "consentDate": "2025-04-14T06:34:58.479Z",
    "_mkto_trk": "id:786-VAD-596&token:_mch-toimitilat.oikotie.fi-759086dc1e900f53e04b66a2f6e89ac3",
}


url = "https://toimitilat.oikotie.fi/api/company"
response = requests.get(url, headers=headers, cookies=cookies)

for item in Company.objects.filter(status='New').order_by('id'):
    name = item.name
    print(f"Processing company: {name}")

    page = 1
    while True:  # Використовуємо while, щоб зупинити обробку, коли сторінки закінчуються
        url = f"https://toimitilat.oikotie.fi/api/company?page={page}&name={name}"

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                json_data = response.json()  # Отримуємо весь JSON відповідь
                print(f"Page {page}: {json_data}")

                # Перевірка на порожні дані
                if not json_data:
                    print("No data found, stopping further requests.")
                    break  # Якщо даних немає, припиняємо цикл

                # Зберігаємо весь JSON в поле json_field
                obj, created = Company.objects.update_or_create(
                    unique_id=json_data.get('id', None),  # Використовуємо 'id' для унікальності
                    defaults={
                        'json_field': json.dumps(json_data)  # Зберігаємо весь JSON у полі json_field
                    }
                )
                print(f"Company {json_data.get('name', 'Unknown')} {'created' if created else 'updated'} successfully!")

                page += 1  # Переходимо до наступної сторінки
            else:
                print(f"Error: Unable to fetch data for page {page}. Status code: {response.status_code}")
                break  # Якщо є помилка з запитом, зупиняємо цикл
        except Exception as e:
            print(f"Error processing company {name}: {e}")
            break  # Якщо виникла помилка в обробці, зупиняємо цикл

    item.status = 'Done'
    item.save()
