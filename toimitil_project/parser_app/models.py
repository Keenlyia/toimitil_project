from django.db import models
import uuid

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Agent(models.Model):
    agent_id = models.BigIntegerField(unique=True, default=1)  # Поле для broker_id
    name = models.CharField(max_length=255, null=True, blank=True)  # Ім'я агента
    email = models.EmailField(null=True, blank=True)  # Email агента
    media_url = models.URLField(null=True, blank=True)  # URL зображення агента
    phone = models.CharField(max_length=20, null=True, blank=True)  # Номер телефону
    url = models.URLField(null=True, blank=True)  # URL профілю агента
    company_media_url = models.URLField(null=True, blank=True)
    company_url = models.URLField(null=True, blank=True)  # URL компанії
    company_name = models.CharField(max_length=255, null=True, blank=True)
    video = models.URLField(null=True, blank=True)  # URL відео (може бути null)
    language_skills = models.CharField(max_length=255, null=True, blank=True)  # Навички мов (може бути null)
    presentation_text = models.TextField(null=True, blank=True)  # Презентація (може бути null)
    specialty = models.CharField(max_length=255, null=True, blank=True)  # Спеціальність (може бути null)
    title = models.CharField(max_length=255, null=True, blank=True)  # Посада агента
    is_visible = models.BooleanField(default=True)  # Статус видимості
    json_field = models.JSONField(null=True, blank=True)  # Поле для зберігання додаткової інформації у форматі JSON
    unique_id = models.CharField(max_length=255, unique=True, null=False, blank=False, default=uuid.uuid4)
    status = models.CharField(max_length=50, null=True, blank=True, default='New')

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=500, null=True, blank=True)
    logo_url = models.URLField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    ad_guarantee = models.BooleanField(default=False)  # Встановлюємо дефолтне значення
    parent_id = models.IntegerField(null=True, blank=True)
    parent_logo_url = models.URLField(null=True, blank=True)
    parent_name = models.CharField(max_length=255, null=True, blank=True)
    unique_id = models.CharField(max_length=255, unique=True, null=False, blank=False, default='0000000')
    json_field = models.JSONField(null=True, blank=True)  # Нове поле для зберігання даних у форматі JSON
    status = models.CharField(max_length=50, default='New')

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name