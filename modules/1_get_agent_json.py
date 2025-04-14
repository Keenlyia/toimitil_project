import requests
from load_django import *
from parser_app.models import *
import json


url = "https://toimitilat.oikotie.fi/api/company/7245253/brokers"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "uk,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "ota-cuid": "3f83ceef360508ccf1c0cc5682f4a2e9998dd8b1",
    "ota-loaded": "1744632190",
    "ota-token": "87509f840cdd650ec8b84b241293bf485da15709220d95d4c311c629ed802e50",
    "priority": "u=1, i",
    "referer": "https://toimitilat.oikotie.fi/yritys/24-housing-oy-konserni/24-housing-espoo-7245253",
    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"10.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

cookies = {
    "PHPSESSID": "c90789ec6ba89c2693eb30ea89f7a181",
    "_sp_su": "false",
    "consentUUID": "706d58f2-35bb-4389-be89-558ea18cacd5_42",
    "consentDate": "2025-04-14T06:34:58.479Z",
    "_mkto_trk": "id:786-VAD-596&token:_mch-toimitilat.oikotie.fi-759086dc1e900f53e04b66a2f6e89ac3",
    "_pulse2data": "868226a4-9211-4f5d-9ce5-13b06e47c2e5%2Cv%2C%2C1745217301000%2CeyJpc3N1ZWRBdCI6IjIwMjUtMDQtMTRUMDY6MzQ6NTlaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsInJlSXNzdWVkQXQiOiIyMDI1LTA0LTE0VDA2OjM1OjAxWiIsImFsZyI6ImRpciIsImtpZCI6IjMifQ..hXf-d9hSSk06SQwh5TRlEg.MgLMpBasZa8uNaULjTFY8yTF_M90qGW61Huz5YJ0R2FrWBUZlie-Yh9LuaVOdlB6YF6sa4RABY8GdNBByHOZrEBL1WNEzld0yuPvM2SI7212NB_1zE0F6BT3PLH1Lq2v5SuB9d1c4F3zypnvSyFs_HGRLMq2zcyBwKvwio8ctql2NuIRY-1NM_0UUz2woylk0xps7RBCB7enz0M3nanLWe5tOou3mfvJIJEcJeiJhY2DKf73f-ayGmxrGRsHQVumOWDtapB9RZ-jZyIFU3Qzg8VWvtHLcKbN5zqSedMx4h1hqZMWcZPNo_tEYZMjYkd3jFPkgkZ51rQ1iwzYub_SaxJpg5AHAnALkH-TRgT5bdnihjHNlReSzIPXBTwVp8l-fLoOSDJ5pQgBpBNCjUQUSsyIjQF7W0673ceCo0xgiB9OpMUzGF1QIvDvkmJ6Bn91AlI0GvYEMQYIPf_VTjmsBgvXUidHhvlecy0Bc51hoIDw2pDMesTQ10f0Nub4q2fI.AntZmDbsoBbTCs5zl-rW5Q%2C1927998293856806667%2C1744626900365%2Ctrue%2C%2CeyJraWQiOiIzIiwiYWxnIjoiSFMyNTYifQ..dE3lXVsf-gKJLZDaakPw66MA173cImbXQh6HRVLdAjU",
    "_gcl_au": "1.1.946569376.1744612622",
    "user_id": "3f83ceef360508ccf1c0cc5682f4a2e9998dd8b1",
    "_pulsesession": "[\"sdrn:schibsted:session:6754545d-352f-42ef-a9d8-9212302bc38c\",1744632165436,1744632165436]",
    "AWSALB": "KZ02cSCkZ52Xho0dmPmTZH015+NfF8bKdb43OniGuvMQU94qTRbZRAXqiXId0o+f3xqCdpVdRf/a1VKVwqazYAozgvIT+w8ORgAebJJyNkvbsMgxYKlhbOQ1OaDe",
    "AWSALBCORS": "KZ02cSCkZ52Xho0dmPmTZH015+NfF8bKdb43OniGuvMQU94qTRbZRAXqiXId0o+f3xqCdpVdRf/a1VKVwqazYAozgvIT+w8ORgAebJJyNkvbsMgxYKlhbOQ1OaDe"
}


response = requests.get(url, headers=headers, cookies=cookies)

if response.status_code == 200:
    data = response.json()
    print("Response JSON:", data)

    # Проходимо по кожному елементу в отриманих даних
    for agent_data in data:
        agent_id = agent_data.get("broker_id")
        agent_name = agent_data.get("name")

        # Створюємо або оновлюємо агентів в базі даних
        agent, created = Agent.objects.update_or_create(
            agent_id=agent_id,
            defaults={
                'name': agent_name,
                'json_field': agent_data  # Зберігаємо JSON
            }
        )

        if created:
            print(f"Agent {agent_name} created")
        else:
            print(f"Agent {agent_name} updated")
else:
    print(f"Request failed with status code {response.status_code}")