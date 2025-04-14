from load_django import *
from parser_app.models import *
import json
import os

export_data = []

# Перебір всіх агентів в json_field
for item in Agent.objects.filter(json_field__isnull=False):

    print()
    print('#' * 50)

    if isinstance(item.json_field, str):
        agent_data = json.loads(item.json_field)
    else:
        agent_data = item.json_field

    name = agent_data.get('name', None)
    print('Agent Name: ', name)

    email = agent_data.get('email', None)
    print('Email: ', email)

    phone = agent_data.get('phone', None)
    print('Phone: ', phone)

    media_url = agent_data.get('media', None)
    print('Media URL: ', media_url)

    profile_url = agent_data.get('profile_url', None)
    print('Profile URL: ', profile_url)

    company_media = agent_data.get('company_media', None)
    print('Company Media URL: ', company_media)

    company_url = agent_data.get('company_url', None)
    print('Company URL: ', company_url)

    company_name = agent_data.get('company_name', None)
    print('Company Name: ', company_name)

    video = agent_data.get('video', None)
    print('Video URL: ', video)

    language_skills = agent_data.get('language_skills', None)
    print('Language Skills: ', language_skills)

    presentation_text = agent_data.get('presentation', None)
    print('Presentation Text: ', presentation_text)

    specialty = agent_data.get('specialty', None)
    print('Specialty: ', specialty)

    title = agent_data.get('title', None)
    print('Title: ', title)

    is_visible = agent_data.get('visible', True)
    print('Is Visible: ', is_visible)

    status = agent_data.get('status', 'New')
    print('Status: ', status)

    unique_id = agent_data.get('unique_id', None)
    print('Unique ID: ', unique_id)

    # Оновлення полів
    item.name = name
    item.email = email
    item.phone = phone
    item.media_url = media_url
    item.url = profile_url
    item.company_media_url = company_media
    item.company_url = company_url
    item.company_name = company_name
    item.video = video
    item.language_skills = language_skills
    item.presentation_text = presentation_text
    item.specialty = specialty
    item.title = title
    item.is_visible = is_visible
    item.status = status

    if unique_id and not Agent.objects.exclude(id=item.id).filter(unique_id=unique_id).exists():
        item.unique_id = unique_id

    item.save()

    # Додаємо до списку для експорту
    export_data.append({
        "name": name,
        "email": email,
        "phone": phone,
        "media_url": media_url,
        "profile_url": profile_url,
        "company_media_url": company_media,
        "company_url": company_url,
        "company_name": company_name,
        "video": video,
        "language_skills": language_skills,
        "presentation_text": presentation_text,
        "specialty": specialty,
        "title": title,
        "is_visible": is_visible,
        "status": status,
        "unique_id": unique_id,
    })

# Зберігаємо у json
with open('../results/agents_data.json', 'w',
          encoding='utf-8') as file:
    json.dump(export_data, file,
              ensure_ascii=False, indent=4)

print("Данні агентів збережено у файл: results/agents_data.json")
